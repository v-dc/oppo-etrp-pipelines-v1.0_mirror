# Spark Connections Guide

This document explains how to use the `spark_factory` and `database_connections` modules to create Spark sessions and manage database connections in the CB-Core system.

## Overview

The CB-Core system provides two main modules for managing Spark sessions and database connections:

1. **`spark_factory.py`** - Creates Spark sessions with different configuration profiles
2. **`database_connections.py`** - Manages database connections and provides utilities for Iceberg catalog configuration

Both modules rely on configuration files located in `spark/configs/`.

## Configuration Files Structure

```
spark/configs/
├── cb_core_base.conf          # Base Spark configuration
├── cb_core_iceberg.conf       # Iceberg catalog configuration
├── cb_core_live.conf          # Live processing configuration (includes iceberg)
├── cb_core_historical.conf    # Historical processing configuration (includes iceberg)
└── database_connections.yaml  # Database connection settings
```

### Configuration Hierarchy

```
cb_core_base.conf
    └── cb_core_iceberg.conf
            ├── cb_core_live.conf
            └── cb_core_historical.conf
```

## Using SparkFactory

The `SparkFactory` class provides multiple ways to create Spark sessions:

### Basic Usage

```python
from common.spark_factory import SparkFactory

# Create a factory instance
factory = SparkFactory()

# Create a basic Spark session
spark = factory.create_session(app_name="MyApp")

# Create an Iceberg-enabled session
spark = factory.create_iceberg_session(app_name="IcebergApp")

# Create a live processing session
spark = factory.create_live_session(app_name="LiveProcessor")

# Create a historical processing session
spark = factory.create_historical_session(app_name="HistoricalProcessor")
```

### Configuration Profiles

SparkFactory supports the following profiles:

- **`base`** - Basic Spark configuration (maps to `cb_core_base.conf`)
- **`iceberg`** - Iceberg catalog support (maps to `cb_core_iceberg.conf`)
- **`live`** - Live data processing (maps to `cb_core_live.conf`)
- **`historical`** - Historical data processing (maps to `cb_core_historical.conf`)

### Custom Configuration

```python
# Use a specific profile
spark = factory.create_session(
    app_name="CustomApp",
    profile="historical"
)

# Override specific configurations
spark = factory.create_session(
    app_name="CustomApp",
    profile="iceberg",
    conf_overrides={
        "spark.sql.shuffle.partitions": "400",
        "spark.executor.memory": "8g"
    }
)
```

## Using Database Connections

The `database_connections` module provides utilities for database connectivity:

### Basic Usage

```python
from common.database_connections import (
    create_spark_session_iceberg,
    get_postgres_connection_properties,
    get_postgres_jdbc_url
)

# Create a Spark session with Iceberg configuration
spark = create_spark_session_iceberg(
    app_name="DataProcessor",
    spark_config="spark_optimized"  # or "spark_minimal"
)

# Get PostgreSQL connection properties
pg_props = get_postgres_connection_properties()
# Returns: {
#     "user": "postgres",
#     "password": "your_password",
#     "driver": "org.postgresql.Driver"
# }

# Get PostgreSQL JDBC URL
jdbc_url = get_postgres_jdbc_url()
# Returns: "jdbc:postgresql://localhost:5433/boards"
```

### Spark Configuration Options

The `database_connections.yaml` file defines two Spark configurations:

1. **`spark_optimized`** - For production workloads
   - 4 executor instances
   - 4GB memory per executor
   - 2 cores per executor
   - Dynamic allocation enabled

2. **`spark_minimal`** - For development/testing
   - 2 executor instances
   - 2GB memory per executor
   - 1 core per executor
   - Dynamic allocation enabled

## Integration Example

Here's a complete example showing how to use both modules together:

```python
from common.spark_factory import SparkFactory
from common.database_connections import get_postgres_connection_properties, get_postgres_jdbc_url

# Method 1: Using SparkFactory for Iceberg operations
factory = SparkFactory()
spark = factory.create_iceberg_session(app_name="DataPipeline")

# Read from Iceberg table
df = spark.table("jdbc_prod.my_table")

# Method 2: Using database_connections for mixed operations
from common.database_connections import create_spark_session_iceberg

spark = create_spark_session_iceberg(
    app_name="ETLPipeline",
    spark_config="spark_optimized"
)

# Read from PostgreSQL
pg_props = get_postgres_connection_properties()
jdbc_url = get_postgres_jdbc_url()

postgres_df = spark.read.jdbc(
    url=jdbc_url,
    table="my_postgres_table",
    properties=pg_props
)

# Write to Iceberg
postgres_df.writeTo("jdbc_prod.my_iceberg_table").createOrReplace()
```

## Configuration Details

### Iceberg Configuration (cb_core_iceberg.conf)

Key settings:
- Catalog implementation: `org.apache.iceberg.spark.SparkCatalog`
- Catalog type: `jdbc`
- JDBC catalog database: `jdbc_catalog_db`
- Warehouse location: `/data2/systems/data/jdbc_warehouse`
- Default file format: Parquet with Snappy compression

### Database Connections (database_connections.yaml)

Contains:
- Iceberg JDBC catalog connection settings
- PostgreSQL operational database connection
- Spark resource allocation profiles

## Best Practices

1. **Choose the right factory method**:
   - Use `create_iceberg_session()` for data lake operations
   - Use `create_live_session()` for real-time processing
   - Use `create_historical_session()` for batch processing

2. **Resource allocation**:
   - Use `spark_optimized` for production workloads
   - Use `spark_minimal` for development/testing

3. **Configuration overrides**:
   - Only override configurations when necessary
   - Document any custom configurations in your code

4. **Error handling**:
   - Both modules will raise exceptions if configuration files are missing
   - Ensure `spark/configs/` directory is in the correct location relative to the modules

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Ensure configuration files exist in `spark/configs/`
2. **Iceberg catalog errors**: Verify PostgreSQL JDBC catalog database is running
3. **Memory issues**: Adjust Spark configuration in `database_connections.yaml`

### Debugging

```python
# Check loaded configuration
factory = SparkFactory()
config = factory._load_config("iceberg")
print(config)

# Verify database connection
from common.database_connections import load_db_config
db_config = load_db_config()
print(db_config['iceberg'])
```