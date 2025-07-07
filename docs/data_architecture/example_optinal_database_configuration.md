# CB-Core Database Configuration

## Overview
CB-Core uses a dual database strategy with PostgreSQL for both Iceberg catalog management and operational analytics.

## Database Architecture

### Iceberg Catalog Database
```
Database: jdbc_catalog_db
Host: localhost:5432
User: jdbc_user
Password: jdbc_password
Purpose: Iceberg table metadata and catalog management
```

### Operational Analytics Database  
```
Database: boards
Host: 192.168.0.74:5432
User: spark_user
Password: spark_password
Purpose: Clean operational data for analytics and reporting
```

## Connection Patterns

### From Spark Applications
```python
# Iceberg catalog connection (built into SparkSession)
spark = SparkSession.builder \
    .appName("CB-Core-Application") \
    .config("spark.sql.catalog.jdbc_prod", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.jdbc_prod.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog") \
    .config("spark.sql.catalog.jdbc_prod.uri", "jdbc:postgresql://localhost:5432/jdbc_catalog_db") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.user", "jdbc_user") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.password", "jdbc_password") \
    .config("spark.sql.catalog.jdbc_prod.warehouse", "/data2/systems/data/jdbc_warehouse") \
    .getOrCreate()

# PostgreSQL operational database connection
jdbc_url = "jdbc:postgresql://192.168.0.74:5432/boards"
connection_properties = {
    "user": "spark_user",
    "password": "spark_password",
    "driver": "org.postgresql.Driver"
}

# Write to operational database
df.write.jdbc(jdbc_url, "table_name", mode="append", properties=connection_properties)
```

### From Python Applications
```python
import psycopg2

# Iceberg catalog connection
catalog_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="jdbc_catalog_db",
    user="jdbc_user",
    password="jdbc_password"
)

# Operational database connection
operational_conn = psycopg2.connect(
    host="192.168.0.74",
    port=5432,
    database="boards",
    user="spark_user",
    password="spark_password"
)
```

## Table Organization

### Iceberg Catalog Tables (jdbc_catalog_db)
- **Purpose**: Metadata storage for Iceberg tables
- **Managed by**: Iceberg framework
- **Access**: Through Spark SQL with jdbc_prod catalog

### Operational Tables (boards database)
```sql
-- Current loan states
CREATE TABLE loans_current (
    loan_id VARCHAR(12) PRIMARY KEY,
    institution_id VARCHAR(10),
    -- ... other fields
);

-- Institution performance metrics
CREATE TABLE institution_performance (
    institution_id VARCHAR(10),
    reporting_period VARCHAR(6),
    -- ... metrics
);

-- Data quality tracking
CREATE TABLE data_quality_summary (
    file_name VARCHAR(200),
    processing_date DATE,
    quality_score DECIMAL(5,2),
    -- ... quality metrics
);
```

## Connection Security

### Credential Management
- **Development**: Hardcoded credentials for NPD server environment
- **Production**: Use environment variables or credential management system
- **Network**: Internal network connections, no external exposure

### Permission Strategy
```sql
-- Iceberg catalog user (jdbc_user)
GRANT ALL PRIVILEGES ON DATABASE jdbc_catalog_db TO jdbc_user;

-- Operational database user (spark_user)  
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO spark_user;
GRANT CREATE ON SCHEMA public TO spark_user;
```

## Performance Considerations

### Connection Pooling
- **Spark**: Managed automatically by Spark SQL engine
- **Direct connections**: Use connection pooling for high-volume applications

### Query Optimization
- **Iceberg**: Leverage partition pruning and file skipping
- **PostgreSQL**: Index key columns (loan_id, institution_id, period)

### Resource Management
```python
# Spark session resource limits
spark_config = {
    'spark.driver.memory': '4g',
    'spark.executor.instances': '2',
    'spark.executor.cores': '3',
    'spark.executor.memory': '8g',
    'spark.executor.memoryOverhead': '2g',
}
```

## Troubleshooting

### Common Connection Issues
1. **Connection refused**: Check if PostgreSQL service is running
2. **Authentication failed**: Verify username/password combinations
3. **Database not found**: Ensure databases exist and are accessible
4. **Network timeout**: Check network connectivity to 192.168.0.74

### Diagnostic Commands
```bash
# Test PostgreSQL service
sudo systemctl status postgresql

# Test network connectivity
ping 192.168.0.74
telnet 192.168.0.74 5432

# Test database access
psql -h localhost -U jdbc_user -d jdbc_catalog_db
psql -h 192.168.0.74 -U spark_user -d boards
```

### Spark-Specific Issues
```python
# Enable Spark SQL logging for debugging
spark.sparkContext.setLogLevel("INFO")

# Test Iceberg catalog connectivity
spark.sql("SHOW DATABASES IN jdbc_prod").show()
spark.sql("SHOW TABLES IN jdbc_prod.default").show()
```

## Development Workflow

### Testing Database Connections
```bash
# Run CB-Core connectivity test
cd /data1/systems/cb-system/cb-core
source /data1/systems/cb-system/venvs-cb/cb3.12/bin/activate
python scripts/operations/test_database_connectivity.py
```

### Creating New Tables
```python
# Iceberg table creation (via Spark)
spark.sql("""
    CREATE TABLE jdbc_prod.default.new_table (
        id bigint,
        name string,
        created_at timestamp
    ) USING iceberg
    PARTITIONED BY (days(created_at))
""")

# PostgreSQL table creation (via Spark or direct SQL)
create_table_sql = """
    CREATE TABLE new_operational_table (
        id SERIAL PRIMARY KEY,
        data_field VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
```

### Data Migration Patterns
```python
# Iceberg to PostgreSQL (staging to operational)
iceberg_df = spark.sql("SELECT * FROM jdbc_prod.default.staging_table")
clean_df = iceberg_df.filter("quality_flag = 'PASSED'")
clean_df.write.jdbc(jdbc_url, "operational_table", mode="append", properties=connection_properties)
```

This configuration supports both development and production use cases while maintaining data integrity and performance.
