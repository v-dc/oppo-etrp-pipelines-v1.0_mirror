# Apache Iceberg on S3 with AWS Glue

## Reference
- [Apache Iceberg Documentation](https://iceberg.apache.org/)
- [AWS Glue Iceberg Support](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-iceberg.html)
- [Iceberg on AWS Best Practices](https://aws.amazon.com/blogs/big-data/getting-started-with-apache-iceberg-on-aws/)

## Purpose
This file explains how Apache Iceberg works with AWS Glue and S3 to provide ACID transactions, schema evolution, and time travel for data lake tables. Covers implementation patterns, benefits, and operational considerations for the eTR+ pipeline.

**Latest Update:** July 2025

---

## What is Apache Iceberg?

### **Table Format Overview**
Apache Iceberg is an **open table format** for large-scale data lakes that provides:
- **ACID Transactions**: Atomic, consistent, isolated, durable operations
- **Schema Evolution**: Add, drop, rename columns without breaking queries
- **Time Travel**: Query data as it existed at any point in time
- **Partition Evolution**: Change partitioning scheme without rewriting data

### **Key Concepts**
- **Metadata Files**: JSON files tracking table schema and file locations
- **Manifest Files**: Lists of data files with partition and column statistics
- **Data Files**: Actual data stored in Parquet, ORC, or Avro format
- **Snapshots**: Point-in-time views of table state

---

## Iceberg Architecture on AWS

### **Storage Layer (S3)**
```
s3://data-lake-bucket/
├── warehouse/
│   └── database_name/
│       └── table_name/
│           ├── metadata/           # Table metadata files
│           │   ├── v1.metadata.json
│           │   ├── v2.metadata.json
│           │   └── snap-xxx.avro
│           ├── data/              # Parquet data files
│           │   ├── year=2024/
│           │   └── year=2025/
│           └── manifests/         # Manifest files
│               └── manifest-xxx.avro
```

### **Catalog Integration**
- **AWS Glue Data Catalog**: Native Iceberg table registration
- **Metadata Storage**: Table schemas, column statistics, partition info
- **Version Control**: Track table schema evolution over time
- **Cross-Service**: Accessible from Glue, EMR, Athena, Redshift

### **Compute Integration**
- **AWS Glue**: Native Iceberg read/write with Spark 3.x
- **Amazon EMR**: Full Iceberg feature support
- **Amazon Athena**: Query Iceberg tables directly
- **Amazon Redshift**: Read Iceberg tables via Spectrum

---

## AWS Glue Iceberg Support

### **Current Capabilities (Glue 5.0)**
- **Iceberg Version**: 1.7.1 support
- **Spark Version**: 3.5.4 with native Iceberg integration
- **Operations**: CREATE, INSERT, UPDATE, DELETE, MERGE
- **Data Formats**: Parquet (primary), ORC, Avro
- **Catalog**: AWS Glue Data Catalog as default metastore

### **Supported Operations**
```python
# Create Iceberg table
df.writeTo("glue_catalog.database.table") \
  .tableProperty("format-version", "2") \
  .tableProperty("write.parquet.compression-codec", "snappy") \
  .using("iceberg") \
  .create()

# Insert data with schema evolution
df.writeTo("glue_catalog.database.table") \
  .option("mergeSchema", "true") \
  .append()

# Time travel queries
spark.read \
  .option("as-of-timestamp", "2024-01-01 00:00:00") \
  .table("glue_catalog.database.table")

# Incremental reads
spark.read \
  .option("start-snapshot-id", "12345") \
  .option("end-snapshot-id", "67890") \
  .table("glue_catalog.database.table")
```

### **Glue Job Configuration**
```python
# Job parameters for Iceberg
job_config = {
    "--enable-glue-datacatalog": "true",
    "--enable-continuous-cloudwatch-log": "true",
    "--iceberg-version": "1.7.1",
    "--spark-version": "3.5.4"
}

# Iceberg-specific settings
spark.conf.set("spark.sql.extensions", 
              "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
spark.conf.set("spark.sql.catalog.glue_catalog", 
              "org.apache.iceberg.spark.SparkCatalog")
spark.conf.set("spark.sql.catalog.glue_catalog.warehouse", 
              "s3://your-bucket/warehouse/")
```

---

## Key Benefits for Data Lakes

### **1. ACID Transactions**
- **Atomicity**: All-or-nothing writes prevent partial updates
- **Consistency**: Readers always see consistent table state
- **Isolation**: Concurrent reads/writes don't interfere
- **Durability**: Committed changes are permanent

### **2. Schema Evolution**
```python
# Add column without breaking existing queries
spark.sql("""
ALTER TABLE glue_catalog.database.transactions 
ADD COLUMN payment_method STRING
""")

# Rename column
spark.sql("""
ALTER TABLE glue_catalog.database.transactions 
RENAME COLUMN amount TO transaction_amount
""")

# Change column type (compatible changes)
spark.sql("""
ALTER TABLE glue_catalog.database.transactions 
ALTER COLUMN customer_id TYPE BIGINT
""")
```

### **3. Time Travel & Versioning**
```python
# Query historical data
historical_df = spark.read \
  .option("as-of-timestamp", "2024-06-01 00:00:00") \
  .table("glue_catalog.database.transactions")

# Compare versions
current_count = spark.table("glue_catalog.database.transactions").count()
yesterday_count = spark.read \
  .option("as-of-timestamp", "2024-07-01 00:00:00") \
  .table("glue_catalog.database.transactions").count()

print(f"New records: {current_count - yesterday_count}")
```

### **4. Efficient Updates & Deletes**
```python
# Update records efficiently
spark.sql("""
UPDATE glue_catalog.database.transactions 
SET status = 'PROCESSED' 
WHERE transaction_date = '2024-07-08' AND status = 'PENDING'
""")

# Delete records (GDPR compliance)
spark.sql("""
DELETE FROM glue_catalog.database.customers 
WHERE customer_id IN (12345, 67890)
""")
```

---

## Partitioning Strategies

### **Partition Evolution**
Iceberg allows changing partition schemes without rewriting data:

```python
# Initial partitioning by date
spark.sql("""
CREATE TABLE glue_catalog.database.transactions (
  transaction_id BIGINT,
  customer_id BIGINT,
  amount DECIMAL(10,2),
  transaction_date DATE,
  created_at TIMESTAMP
) USING iceberg
PARTITIONED BY (days(transaction_date))
""")

# Evolve to partition by date + customer segment
spark.sql("""
ALTER TABLE glue_catalog.database.transactions 
ADD PARTITION FIELD bucket(customer_id, 10)
""")
```

### **Partition Types**
- **Identity**: `PARTITIONED BY (region)`
- **Date/Time**: `PARTITIONED BY (days(event_time))`
- **Bucketing**: `PARTITIONED BY (bucket(customer_id, 16))`
- **Truncation**: `PARTITIONED BY (truncate(email, 10))`

### **Best Practices**
- **Avoid High Cardinality**: Don't partition by unique values
- **Query Patterns**: Partition by commonly filtered columns
- **File Size**: Target 100MB-1GB files per partition
- **Evolution**: Start simple, evolve based on usage patterns

---

## Performance Optimizations

### **File Management**
```python
# Compact small files
spark.sql("""
CALL glue_catalog.system.rewrite_data_files(
  table => 'database.table',
  target_file_size_bytes => 134217728  -- 128MB
)
""")

# Rewrite manifests
spark.sql("""
CALL glue_catalog.system.rewrite_manifests('database.table')
""")

# Expire old snapshots
spark.sql("""
CALL glue_catalog.system.expire_snapshots(
  table => 'database.table',
  older_than => TIMESTAMP '2024-06-01 00:00:00'
)
""")
```

### **Query Optimization**
- **Predicate Pushdown**: Iceberg pushes filters to file level
- **Column Pruning**: Only read required columns
- **Min/Max Statistics**: Skip files based on column ranges
- **Bloom Filters**: Reduce false positives for equality predicates

### **Write Optimizations**
```python
# Optimize write performance
df.write \
  .format("iceberg") \
  .option("write.parquet.compression-codec", "zstd") \
  .option("write.target-file-size-bytes", "134217728") \
  .option("write.fanout.enabled", "true") \
  .mode("append") \
  .saveAsTable("glue_catalog.database.table")
```

---

## Integration with eTR+ Pipeline

### **Data Architecture Pattern**
```python
# Raw data ingestion (Bronze layer)
raw_df.write \
  .format("iceberg") \
  .option("write.format.default", "parquet") \
  .mode("append") \
  .saveAsTable("glue_catalog.bronze.bnpl_transactions_raw")

# Cleaned data (Silver layer)
cleaned_df.write \
  .format("iceberg") \
  .option("mergeSchema", "true") \
  .mode("overwrite") \
  .option("partitionOverwriteMode", "dynamic") \
  .saveAsTable("glue_catalog.silver.bnpl_transactions_clean")

# Aggregated data (Gold layer)
aggregated_df.write \
  .format("iceberg") \
  .mode("overwrite") \
  .saveAsTable("glue_catalog.gold.bnpl_daily_summary")
```

### **GDPR Compliance Example**
```python
# Handle right to be forgotten
def delete_customer_data(customer_id):
    # Delete from all relevant tables
    tables = [
        "bronze.bnpl_transactions_raw",
        "silver.bnpl_transactions_clean", 
        "gold.customer_profiles"
    ]
    
    for table in tables:
        spark.sql(f"""
        DELETE FROM glue_catalog.{table} 
        WHERE customer_id = {customer_id}
        """)
    
    # Create audit record
    audit_df = spark.createDataFrame([
        (customer_id, "GDPR_DELETE", datetime.now())
    ], ["customer_id", "action", "timestamp"])
    
    audit_df.write \
      .format("iceberg") \
      .mode("append") \
      .saveAsTable("glue_catalog.audit.gdpr_actions")
```

### **Data Quality Integration**
```python
# Validate data quality with time travel
def validate_data_quality(table_name, validation_timestamp):
    # Current state
    current_df = spark.table(f"glue_catalog.silver.{table_name}")
    
    # Historical state for comparison
    historical_df = spark.read \
      .option("as-of-timestamp", validation_timestamp) \
      .table(f"glue_catalog.silver.{table_name}")
    
    # Quality checks
    current_count = current_df.count()
    historical_count = historical_df.count()
    
    # Log quality metrics
    quality_metrics = spark.createDataFrame([
        (table_name, "record_count", current_count, datetime.now()),
        (table_name, "daily_growth", current_count - historical_count, datetime.now())
    ], ["table_name", "metric", "value", "measured_at"])
    
    quality_metrics.write \
      .format("iceberg") \
      .mode("append") \
      .saveAsTable("glue_catalog.monitoring.data_quality_metrics")
```

---

## Operational Considerations

### **Maintenance Tasks**
```python
# Automated maintenance job
def iceberg_maintenance(table_name):
    # 1. Compact small files
    spark.sql(f"""
    CALL glue_catalog.system.rewrite_data_files(
      table => '{table_name}',
      target_file_size_bytes => 134217728
    )
    """)
    
    # 2. Rewrite manifests for better query performance
    spark.sql(f"""
    CALL glue_catalog.system.rewrite_manifests('{table_name}')
    """)
    
    # 3. Expire old snapshots (keep 30 days)
    expiry_date = datetime.now() - timedelta(days=30)
    spark.sql(f"""
    CALL glue_catalog.system.expire_snapshots(
      table => '{table_name}',
      older_than => TIMESTAMP '{expiry_date}'
    )
    """)
```

### **Monitoring & Alerting**
- **File Count**: Monitor for small file proliferation
- **Snapshot Growth**: Track metadata growth over time
- **Query Performance**: Monitor scan data volumes
- **Compaction Jobs**: Schedule regular maintenance

### **Backup & Recovery**
- **Metadata Backup**: Iceberg metadata is self-contained
- **Point-in-Time Recovery**: Use time travel for data recovery
- **Cross-Region**: Replicate critical tables across regions
- **Versioning**: Multiple snapshots provide natural backup points

---

## Common Pitfalls & Solutions

### **1. Small Files Problem**
**Issue**: Many small files degrade query performance
**Solution**: 
- Regular compaction jobs
- Tune `write.target-file-size-bytes`
- Use `write.fanout.enabled` for high-cardinality partitions

### **2. Metadata Growth**
**Issue**: Too many snapshots increase metadata size
**Solution**:
- Regular `expire_snapshots` calls
- Reasonable snapshot retention (7-30 days)
- Monitor manifest file counts

### **3. Concurrent Writes**
**Issue**: Multiple writers can cause conflicts
**Solution**:
- Use optimistic concurrency control
- Implement retry logic for conflicts
- Consider write coordination patterns

### **4. Schema Evolution Compatibility**
**Issue**: Breaking schema changes
**Solution**:
- Plan schema changes carefully
- Use compatible type promotions only
- Test schema evolution in non-production

---

## Performance Benchmarks

### **Query Performance Improvements**
| Operation | Traditional Parquet | Iceberg on S3 | Improvement |
|-----------|-------------------|---------------|-------------|
| **Full Table Scan** | 100% | 95% | 5% faster |
| **Predicate Pushdown** | 100% | 40% | 60% less data |
| **Column Pruning** | 100% | 30% | 70% less I/O |
| **Time Travel Query** | Not possible | Available | New capability |
| **Updates/Deletes** | Full rewrite | Incremental | 10x faster |

### **Storage Efficiency**
- **Compression**: Parquet with column-level compression
- **Deduplication**: Automatic small file consolidation
- **Metadata Overhead**: ~1-2% of total data size
- **Versioning**: Incremental storage for changes only

---

## Cost Considerations

### **Storage Costs**
- **S3 Standard**: $0.025/GB/month (ap-southeast-5)
- **Metadata Files**: Minimal overhead (~1-2%)
- **Lifecycle Policies**: Move old snapshots to IA/Glacier
- **Compression**: 60-80% size reduction vs. raw data

### **Compute Costs**
- **Glue DPU Hours**: Standard Glue pricing applies
- **Query Efficiency**: Reduced I/O lowers compute costs
- **Maintenance Jobs**: Budget for compaction and cleanup
- **Cross-Service**: No additional costs for Athena/EMR access

### **Cost Optimization**
```python
# Optimize for cost
iceberg_options = {
    "write.parquet.compression-codec": "zstd",  # Better compression
    "write.target-file-size-bytes": "268435456",  # 256MB files
    "commit.retry.num-retries": "3",  # Reduce conflicts
    "write.metadata.delete-after-commit.enabled": "true"  # Cleanup
}
```

---

## Regional Availability (Malaysia ap-southeast-5)

| Component | Available | Version | Notes |
|-----------|-----------|---------|--------|
| **AWS Glue Iceberg** | ✅ Yes | 1.7.1 | Full feature support |
| **S3 Storage** | ✅ Yes | - | Standard S3 capabilities |
| **Glue Data Catalog** | ✅ Yes | - | Native Iceberg registration |
| **Amazon Athena** | ✅ Yes | - | Direct Iceberg querying |
| **Amazon EMR** | ✅ Yes | - | Full Iceberg ecosystem |

### **Getting Started Checklist**
- [ ] Enable Glue Data Catalog in target region
- [ ] Configure S3 bucket with appropriate lifecycle policies
- [ ] Set up IAM roles for Glue jobs with S3/Catalog permissions
- [ ] Create initial database schema in Glue Catalog
- [ ] Deploy sample Iceberg table creation job
- [ ] Set up monitoring for table maintenance needs

> **Recommendation**: Start with simple append-only tables to learn Iceberg patterns, then evolve to more complex operations like updates, deletes, and schema evolution as team expertise grows.