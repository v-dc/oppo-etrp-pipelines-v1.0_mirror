#!/usr/bin/env python3
"""
Test Spark job for Airflow database connectivity validation
This job tests database connections when submitted via Airflow
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from pyspark.sql import SparkSession
    from common.database_connections import create_spark_session_iceberg, get_postgres_connection_properties, get_postgres_jdbc_url
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_airflow_database_connectivity():
    """Test database connectivity from Airflow-submitted Spark job"""
    print("=== Airflow Database Connectivity Test ===")
    
    spark = None
    try:
        # Create Spark session with Iceberg configuration
        spark = create_spark_session_iceberg("airflow-db-test", "spark_minimal")
        print("✅ Spark session created from Airflow job")
        
        # Test basic Spark operation
        test_df = spark.range(3)
        count = test_df.count()
        print(f"✅ Basic Spark operation successful (count: {count})")
        
        # Test PostgreSQL connectivity
        jdbc_url = get_postgres_jdbc_url()
        connection_properties = get_postgres_connection_properties()
        
        # Create test data
        test_data = [
            ("airflow_test", datetime.now().isoformat(), "SUCCESS"),
            ("connectivity", datetime.now().isoformat(), "VALIDATED")
        ]
        
        test_df = spark.createDataFrame(test_data, ["test_type", "timestamp", "status"])
        
        # Write to PostgreSQL
        test_df.write \
            .jdbc(jdbc_url, "cb_core_airflow_test", mode="overwrite", 
                  properties=connection_properties)
        
        print("✅ Airflow → Spark → PostgreSQL write successful")
        
        # Read back the data
        read_df = spark.read \
            .jdbc(jdbc_url, "cb_core_airflow_test", properties=connection_properties)
        
        read_count = read_df.count()
        print(f"✅ Airflow → Spark → PostgreSQL read successful (records: {read_count})")
        
        # Test Iceberg operations (basic)
        try:
            # Create a simple test with Iceberg
            spark.sql("SHOW NAMESPACES IN jdbc_prod").show()
            print("✅ Iceberg catalog accessible from Airflow job")
        except Exception as e:
            print(f"⚠️  Iceberg catalog warning from Airflow: {e}")
        
        print("\n🎉 Airflow database connectivity test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Airflow database connectivity test failed: {e}")
        return False
    finally:
        if spark:
            spark.stop()
            print("✅ Spark session stopped")


if __name__ == "__main__":
    success = test_airflow_database_connectivity()
    sys.exit(0 if success else 1)
