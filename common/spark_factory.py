"""
CB-Core Spark Session Factory
Provides standardized Spark session creation with CB-Core configurations
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from pyspark.sql import SparkSession


class CBSparkSessionFactory:
    """Factory for creating CB-Core optimized Spark sessions"""
    
    # Configuration file mappings
    CONFIG_PROFILES = {
        'base': 'cb_core_base.conf',
        'development': 'cb_core_development.conf', 
        'iceberg': 'cb_core_iceberg.conf',
        'historical': 'cb_core_historical.conf',
        'live': 'cb_core_live.conf'
    }
    
    @staticmethod
    def get_config_path(profile: str = 'base') -> str:
        """Get path to configuration file"""
        cb_core_root = Path(__file__).parent.parent.parent
        config_file = CBSparkSessionFactory.CONFIG_PROFILES.get(profile, 'cb_core_base.conf')
        return str(cb_core_root / 'spark' / 'configs' / config_file)
    
    @staticmethod
    def load_spark_config(profile: str = 'base') -> Dict[str, str]:
        """Load Spark configuration from file"""
        config = {}
        config_path = CBSparkSessionFactory.get_config_path(profile)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Spark config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('include'):
                    if '=' in line or ' ' in line:
                        # Handle both = and space-separated configs
                        parts = line.replace('=', ' ').split(None, 1)
                        if len(parts) == 2:
                            key, value = parts
                            config[key] = value
        
        return config
    
    @staticmethod
    def create_session(
        app_name: str,
        profile: str = 'base',
        additional_config: Optional[Dict[str, str]] = None
    ) -> SparkSession:
        """
        Create Spark session with CB-Core configuration
        
        Args:
            app_name: Application name for Spark session
            profile: Configuration profile (base, development, iceberg, historical, live)
            additional_config: Additional Spark configurations to apply
            
        Returns:
            Configured SparkSession
        """
        # Load base configuration
        config = CBSparkSessionFactory.load_spark_config(profile)
        
        # Override app name
        config['spark.app.name'] = f"CB-Core-{app_name}"
        
        # Add additional configurations
        if additional_config:
            config.update(additional_config)
        
        # Create Spark session builder
        builder = SparkSession.builder
        
        # Apply all configurations
        for key, value in config.items():
            builder = builder.config(key, value)
        
        # Create session
        spark = builder.getOrCreate()
        
        # Set log level for CB-Core
        spark.sparkContext.setLogLevel("WARN")
        
        return spark
    
    @staticmethod
    def create_iceberg_session(app_name: str, additional_config: Optional[Dict[str, str]] = None) -> SparkSession:
        """Create Spark session optimized for Iceberg operations"""
        return CBSparkSessionFactory.create_session(app_name, profile='iceberg', additional_config=additional_config)
    
    @staticmethod
    def create_development_session(app_name: str) -> SparkSession:
        """Create Spark session for development with minimal resources"""
        return CBSparkSessionFactory.create_session(app_name, profile='development')
    
    @staticmethod
    def create_historical_session(app_name: str) -> SparkSession:
        """Create Spark session for historical data processing"""
        return CBSparkSessionFactory.create_session(app_name, profile='historical')
    
    @staticmethod
    def create_live_session(app_name: str) -> SparkSession:
        """Create Spark session for live data processing"""
        return CBSparkSessionFactory.create_session(app_name, profile='live')


# Convenience functions for common use cases
def create_spark_session(app_name: str, profile: str = 'iceberg') -> SparkSession:
    """
    Create CB-Core Spark session with specified profile
    
    Args:
        app_name: Application name
        profile: Configuration profile
        
    Returns:
        Configured SparkSession
    """
    return CBSparkSessionFactory.create_session(app_name, profile)


def create_iceberg_session(app_name: str) -> SparkSession:
    """Create Iceberg-optimized Spark session"""
    return CBSparkSessionFactory.create_iceberg_session(app_name)


def create_development_session(app_name: str) -> SparkSession:
    """Create development Spark session"""
    return CBSparkSessionFactory.create_development_session(app_name)


# Example usage:
if __name__ == "__main__":
    # Test session creation
    spark = create_iceberg_session("test-session")
    print(f"Created Spark session: {spark.sparkContext.appName}")
    print(f"Spark version: {spark.version}")
    
    # Test basic functionality
    test_df = spark.range(10)
    print(f"Test DataFrame count: {test_df.count()}")
    
    spark.stop()
