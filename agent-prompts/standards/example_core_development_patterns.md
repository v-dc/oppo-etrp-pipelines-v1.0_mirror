# CB-Core Development Patterns for Claude Code

## Overview
Specific patterns and conventions for CB-Core development to ensure consistency.

## File Organization Patterns

### Module Structure
```
src/
├── module_name/
│   ├── __init__.py
│   ├── processor.py      # Main processing logic
│   ├── validator.py      # Data validation
│   └── utils.py          # Utility functions
```

### DAG Organization
```
airflow/dags/
├── live_processing/
│   └── live_module_dag.py
├── historical_processing/
│   └── historical_module_dag.py
├── common/
│   └── shared_tasks.py
└── test/
    └── test_connectivity_dag.py
```

## Naming Conventions

### DAG Names
```python
# Pattern: cb_core_{type}_{module}
'cb_core_live_ingestion'
'cb_core_historical_ingestion'
'cb_core_test_connectivity'
```

### Task IDs
```python
# Pattern: {action}_{object}
'check_input_files'
'process_credit_files'
'validate_data_quality'
'write_to_iceberg'
'update_postgres'
```

### Spark Job Names
```python
# Pattern: CB-Core-{Module}-{Action}
name='CB-Core-Ingestion-Historical'
name='CB-Core-Quality-Validation'
name='CB-Core-Transform-Customer'
```

## Iceberg Table Creation Patterns

### Always Use PySpark for Iceberg Tables
- **Never use raw SQL DDL** for Iceberg table creation
- **Always use PySpark** with proper JDBC catalog configuration
- Use `CBSparkSessionFactory.create_iceberg_session()` for all Iceberg operations

### Required Pattern for Table Creation
```python
from common.spark_factory import CBSparkSessionFactory

# Create Iceberg-enabled Spark session
spark = CBSparkSessionFactory.create_iceberg_session("app-name")

# Create table using PySpark SQL
spark.sql("""
    CREATE OR REPLACE TABLE jdbc_prod.default.table_name (
        column1 STRING NOT NULL,
        column2 BIGINT,
        -- ... other columns
    ) USING ICEBERG
    PARTITIONED BY (partition_column)
    TBLPROPERTIES (
        'write.format.default' = 'parquet',
        'write.parquet.compression-codec' = 'snappy'
    )
""")
```

### JDBC Catalog Configuration
- Catalog name: `jdbc_prod` (configured in spark/configs/cb_core_iceberg.conf)
- Default schema: `default`
- Full table reference: `jdbc_prod.default.table_name`
- Configuration automatically loaded via `create_iceberg_session()`

### Common Mistake to Avoid
- ❌ Writing raw DDL files without PySpark execution
- ✅ Using PySpark with proper catalog configuration

## Data Processing Patterns

### File Processing Workflow
```python
# Standard CB-Core file processing pattern
file_check >> schema_validation >> quality_check >> process_data >> write_staging >> validate_output >> write_operational
```

### Correlation ID Usage
```python
# Always generate correlation ID for tracking
correlation_id = str(uuid.uuid4())
logger = logging.LoggerAdapter(logger, {'correlation_id': correlation_id})

# Include in Spark job name
name=f'CB-Core-Job-{correlation_id[:8]}'
```

### Error Handling Pattern
```python
def main():
    spark = None
    try:
        spark = create_spark_session("job-name")
        # Processing logic
        logger.info("Job completed successfully")
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")
        # Write to quarantine if applicable
        raise
    finally:
        if spark:
            spark.stop()
```

## Configuration Patterns

### Spark Configuration
```python
# Standard CB-Core Spark config
conf = {
    'spark.driver.memory': '4g',
    'spark.executor.instances': '2',
    'spark.executor.cores': '3',
    'spark.executor.memory': '8g',
    'spark.executor.memoryOverhead': '2g',
}

# Add Iceberg config when needed
iceberg_conf = {
    'spark.sql.catalog.jdbc_prod': 'org.apache.iceberg.spark.SparkCatalog',
    'spark.sql.catalog.jdbc_prod.catalog-impl': 'org.apache.iceberg.jdbc.JdbcCatalog',
    'spark.sql.catalog.jdbc_prod.uri': 'jdbc:postgresql://localhost:5432/jdbc_catalog_db',
    'spark.sql.catalog.jdbc_prod.jdbc.user': 'jdbc_user',
    'spark.sql.catalog.jdbc_prod.jdbc.password': 'jdbc_password',
    'spark.sql.catalog.jdbc_prod.warehouse': '/data2/systems/data/jdbc_warehouse',
}
```

### Database Connection Pattern
```python
# PostgreSQL operational database
jdbc_url = "jdbc:postgresql://192.168.0.74:5432/boards"
connection_properties = {
    "user": "spark_user",
    "password": "spark_password",
    "driver": "org.postgresql.Driver"
}
```

## Testing Patterns

### Test File Structure
```python
# tests/unit/test_module_name.py
class TestModuleName:
    def test_function_name(self):
        # Test implementation
        pass
    
    @pytest.mark.spark
    def test_with_spark(self, spark_session):
        # Spark-specific test
        pass
```

### Integration Test Pattern
```python
@pytest.mark.integration
@pytest.mark.database
class TestDatabaseIntegration:
    def test_end_to_end_flow(self):
        # Complete flow test
        pass
```

## Data Quality Patterns

### Great Expectations Integration
```python
def validate_with_ge(df: DataFrame, suite_name: str) -> bool:
    """Standard GE validation pattern"""
    runner = CBDataQualityRunner()
    results = runner.validate_dataframe(df, suite_name)
    
    if not results["success"]:
        # Write to quarantine
        write_to_quarantine(df, f"quality_failure_{suite_name}")
        return False
    
    return True
```

### Data Flow Pattern
```
Raw Data → Schema Validation → Business Rules → Quality Scoring → Iceberg Staging → Manual Review → PostgreSQL Clean
```

## Logging Patterns

### Structured Logging
```python
import logging
import uuid
from datetime import datetime

# Setup logger with correlation ID
correlation_id = str(uuid.uuid4())
logger = logging.LoggerAdapter(
    logging.getLogger(__name__),
    {
        'correlation_id': correlation_id,
        'job_type': 'ingestion',
        'institution_type': 'BK'
    }
)

# Log with structured data
logger.info("Processing started", extra={
    "file_count": 50,
    "processing_date": datetime.now().isoformat()
})
```

## Resource Management Patterns

### Exclusive Processing
```python
# Live processing (active during business hours)
live_dag = DAG(
    'cb_core_live_processing',
    schedule='0 6 * * *',  # 6 AM daily
    is_paused_upon_creation=False,
    max_active_runs=1,  # Prevent overlapping runs
)

# Historical processing (manual activation)
historical_dag = DAG(
    'cb_core_historical_processing', 
    schedule=None,  # Manual only
    is_paused_upon_creation=True,
    max_active_runs=1,
)
```

### Resource Allocation
```python
# Use 7/8 cores, 24/32 GB memory (leave buffer for OS)
spark_config = {
    'spark.driver.memory': '4g',
    'spark.driver.cores': '1',
    'spark.executor.instances': '2',
    'spark.executor.cores': '3',
    'spark.executor.memory': '8g',
    'spark.executor.memoryOverhead': '2g',
}
```

## Documentation Patterns

### Function Documentation
```python
def process_credit_bureau_file(file_path: str, institution_type: str) -> DataFrame:
    """
    Process credit bureau file according to CB-Core standards.
    
    Args:
        file_path: Full path to pipe-delimited credit bureau file
        institution_type: Institution type (BK/MG/LN/FS/OT)
        
    Returns:
        DataFrame with validated and enriched credit bureau data
        
    Raises:
        ValidationError: If file doesn't meet quality standards
        ProcessingError: If processing fails
    """
```

### Module Documentation
```python
"""
CB-Core Credit Bureau File Ingestion Module

This module handles the ingestion of credit bureau files from financial institutions,
processing them through validation, quality checks, and loading into both Iceberg
staging and PostgreSQL operational databases.

Key Features:
- 63-field pipe-delimited file processing
- Institution-specific validation rules
- Great Expectations quality framework integration
- Dual storage strategy (Iceberg + PostgreSQL)

Usage:
    from src.ingestion.credit_bureau_processor import process_files
    
    # Process files for specific institution
    results = process_files(
        input_path="/data1/systems/cb-system/data/raw-incoming/",
        institution_type="BK"
    )
"""
```

## Integration Patterns

### Cross-Module Communication
```python
# Use shared data structures
from src.common.data_models import CreditBureauRecord, ProcessingResult

# Consistent return types
def process_module() -> ProcessingResult:
    return ProcessingResult(
        success=True,
        records_processed=1000,
        quality_score=95.5,
        correlation_id=correlation_id
    )
```

### Configuration Management
```python
# Use centralized configuration
from src.common.config import CBCoreConfig

config = CBCoreConfig()
spark_session = config.create_spark_session("module-name")
db_connection = config.get_postgres_connection()
```

These patterns ensure consistency across all CB-Core development and help Claude Code generate code that fits seamlessly into the existing architecture.
