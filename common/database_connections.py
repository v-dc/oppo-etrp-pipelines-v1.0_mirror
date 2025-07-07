"""
CB-Core Database Connection Utilities
Standard database connection patterns for CB-Core
"""

import yaml
import os
from typing import Dict, Any
from pyspark.sql import SparkSession


def load_db_config() -> Dict[str, Any]:
    """Load database configuration from YAML file"""
    config_path = os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "spark", "configs", "database_connections.yaml"
    )
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session_iceberg(app_name: str, config_type: str = "spark_optimized") -> SparkSession:
    """Create Spark session configured for Iceberg"""
    config = load_db_config()
    iceberg_config = config['iceberg_catalog']
    spark_config = config[config_type]
    
    builder = SparkSession.builder.appName(f"CB-Core-{app_name}")
    
    # Add Spark configuration
    for key, value in spark_config.items():
        builder = builder.config(f"spark.{key.replace('_', '.')}", str(value))
    
    # Add Iceberg configuration
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}", 
                           "org.apache.iceberg.spark.SparkCatalog")
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.catalog-impl", 
                           iceberg_config['catalog_impl'])
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.uri", 
                           iceberg_config['jdbc_uri'])
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.jdbc.user", 
                           iceberg_config['jdbc_user'])
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.jdbc.password", 
                           iceberg_config['jdbc_password'])
    builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.warehouse", 
                           iceberg_config['warehouse_path'])
    
    # Add Iceberg properties
    for key, value in iceberg_config['properties'].items():
        builder = builder.config(f"spark.sql.catalog.{iceberg_config['catalog_name']}.{key}", value)
    
    return builder.getOrCreate()


def get_postgres_connection_properties() -> Dict[str, str]:
    """Get PostgreSQL connection properties for Spark JDBC"""
    config = load_db_config()
    pg_config = config['postgresql_operational']
    
    return {
        "user": pg_config['user'],
        "password": pg_config['password'],
        "driver": pg_config['driver'],
        **pg_config.get('properties', {})
    }


def get_postgres_jdbc_url() -> str:
    """Get PostgreSQL JDBC URL"""
    config = load_db_config()
    return config['postgresql_operational']['jdbc_url']
