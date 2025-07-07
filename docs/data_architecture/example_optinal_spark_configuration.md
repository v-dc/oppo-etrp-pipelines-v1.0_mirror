# CB-Core Spark Configuration

## Overview
CB-Core uses profile-based Spark configurations optimized for NPD server resources and different processing modes.

## Configuration Profiles

### Base Configuration (cb_core_base.conf)
- **Purpose**: Default configuration for general CB-Core applications
- **Resources**: 7/8 cores, 20/32GB memory
- **Use case**: Standard data processing operations

### Development Configuration (cb_core_development.conf)
- **Purpose**: Minimal resource allocation for development and testing
- **Resources**: 3/8 cores, 6/32GB memory
- **Use case**: Local development, unit testing, debugging

### Iceberg Configuration (cb_core_iceberg.conf)
- **Purpose**: Extends base configuration with Iceberg catalog settings
- **Resources**: Same as base + Iceberg optimizations
- **Use case**: Data lake operations, staging data processing

### Historical Configuration (cb_core_historical.conf)
- **Purpose**: Maximum resource allocation for batch historical processing
- **Resources**: 7/8 cores, 26/32GB memory
- **Use case**: Processing 19,976 historical files

### Live Configuration (cb_core_live.conf)
- **Purpose**: Optimized for real-time, low-latency processing
- **Resources**: 7/8 cores, 20/32GB memory with latency optimizations
- **Use case**: Real-time file processing, streaming data

## Resource Allocation Strategy

### NPD Server Specifications
- **CPU**: Intel Xeon E-2378 (8 cores/16 threads)
- **Memory**: 32GB ECC
- **Storage**: 960GB SSD + 2×2TB HDD

### Resource Distribution
```
Component               Cores    Memory    Purpose
Driver                  1        4-6GB     Coordination and small tasks
Executor 1              3        8-10GB    Parallel processing
Executor 2              3        8-10GB    Parallel processing
OS Buffer               1        6-8GB     System operations
Total Allocated         7/8      20-26/32GB
```

## Usage Patterns

### Using Spark Session Factory
```python
from src.common.spark_factory import CBSparkSessionFactory

# Create session with specific profile
spark = CBSparkSessionFactory.create_session("my-app", profile="iceberg")

# Or use convenience methods
spark = CBSparkSessionFactory.create_iceberg_session("my-app")
spark = CBSparkSessionFactory.create_development_session("my-app")
spark = CBSparkSessionFactory.create_historical_session("my-app")
spark = CBSparkSessionFactory.create_live_session("my-app")
```

### Direct Configuration Loading
```python
# Load configuration manually
config = CBSparkSessionFactory.load_spark_config("historical")

# Apply to custom Spark session
builder = SparkSession.builder
for key, value in config.items():
    builder = builder.config(key, value)
spark = builder.getOrCreate()
```

### Airflow Integration
```python
# In Airflow DAGs
spark_task = SparkSubmitOperator(
    task_id='process_data',
    application='/data1/systems/cb-system/cb-core/src/module/job.py',
    name='CB-Core-Job-Name',
    conf={
        # Use profile-specific configurations
        'spark.driver.memory': '4g',
        'spark.executor.instances': '2',
        'spark.executor.cores': '3',
        'spark.executor.memory': '8g',
    },
    py_files='/data1/systems/cb-system/cb-core/src',
    dag=dag,
)
```

## Performance Optimization

### Single-Node Optimizations
- **Adaptive Query Execution**: Enabled for dynamic optimization
- **Coalescing Partitions**: Reduces small file overhead
- **Skew Join Handling**: Optimizes uneven data distribution
- **Vectorized Processing**: Enabled for Iceberg and Parquet

### Memory Management
- **Storage Level**: MEMORY_AND_DISK_SER for efficient serialization
- **Compression**: Enabled for RDD, shuffle, and storage
- **Memory Overhead**: 20-30% buffer for off-heap operations

### File Processing Optimizations
- **Partition Sizing**: 256MB target for optimal processing
- **Broadcast Joins**: Automatic for tables < 100-200MB
- **File Skipping**: Leverages Iceberg metadata for pruning

## Configuration Files Location

```
spark/configs/
├── cb_core_base.conf          # Base configuration
├── cb_core_development.conf   # Development profile  
├── cb_core_iceberg.conf       # Iceberg-enabled profile
├── cb_core_historical.conf    # Historical processing
└── cb_core_live.conf          # Live processing
```

## Monitoring and Logging

### Spark UI Access
- **Port**: 4040 (base), 4041 (development)
- **URL**: http://192.168.0.74:4040
- **Features**: Job tracking, stage analysis, storage monitoring

### Event Logging
- **Location**: `/data1/systems/cb-system/logs/spark-events`
- **Purpose**: Historical analysis and debugging
- **Retention**: Managed manually

### Application Logs
- **Location**: Integrated with CB-Core logging framework
- **Format**: Structured JSON with correlation IDs
- **Level**: WARN (default) or INFO (debugging)

## Troubleshooting

### Common Issues

#### Out of Memory Errors
```bash
# Symptoms: OutOfMemoryError, GC overhead
# Solution: Reduce executor memory or increase memoryOverhead
spark.executor.memory              6g
spark.executor.memoryOverhead      3g
```

#### Slow Performance
```bash
# Check partition count and size
spark.sql.shuffle.partitions       100  # Reduce for small data
spark.sql.files.maxPartitionBytes  134217728  # 128MB for smaller files
```

#### Iceberg Connectivity Issues
```bash
# Verify catalog configuration
spark.sql.catalog.jdbc_prod.uri    jdbc:postgresql://localhost:5432/jdbc_catalog_db
# Check warehouse permissions
ls -la /data2/systems/data/jdbc_warehouse
```

### Validation Tools
```bash
# Test all configurations
cd /data1/systems/cb-system/cb-core
python scripts/operations/validate_spark_configuration.py

# Test specific profile
python -c "
from src.common.spark_factory import create_iceberg_session
spark = create_iceberg_session('test')
print(f'Success: {spark.sparkContext.appName}')
spark.stop()
"
```

This configuration framework provides flexible, optimized Spark environments for all CB-Core processing scenarios while maximizing NPD server resource utilization.
