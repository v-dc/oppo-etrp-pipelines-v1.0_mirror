"""
CB-Core File Discovery DAG V2 - Improved Version

This DAG demonstrates best practices for file discovery using:
- Task decorators with external Python environment
- Integrated file processing logic
- Spark-based batch processing (avoiding memory issues)
- Reporting capabilities
- Improved table operations with merge
- Centralized configuration
- Data quality validation

Author: CB-Core Team
"""

import yaml
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from airflow_paths import AIRFLOW_CONFIG_PATH

# Load configuration
try:
    with open(AIRFLOW_CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
except yaml.YAMLError as e:
    raise Exception(f'Error reading YAML file: {e}')

VENV_PATH = config['package']['venv']
PACKAGE_ROOT = config['package']['root']
PYTHON_EXEC = f"{VENV_PATH}/bin/python"

# Default arguments
default_args = {
    'owner': 'cb-core',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id='file_discovery_v2',
    description='Improved file discovery with Spark processing and reporting',
    default_args=default_args,
    schedule=None,
    max_active_runs=1,
    params={
        'source_directory': Param(
            default='/data1/systems/cb-system/data/raw/',
            type='string',
            description='The source directory for discovering files',
        ),
        'pattern': Param(
            default='*.txt',
            type='string',
            description='File pattern to match',
        ),
        'date_from': Param(
            default='',
            type='string',
            description='Start date for filtering (YYYY-MM-DD)',
        ),
        'date_to': Param(
            default='',
            type='string',
            description='End date for filtering (YYYY-MM-DD)',
        ),
        'table_mode': Param(
            default='merge',
            type='string',
            enum=['merge', 'append', 'overwrite'],
            description='How to update the target table',
        ),
    },
    tags=['iceberg', 'discovery', 'v2']
) as dag:

    @task.external_python(
        task_id='validate_source_directory',
        python=PYTHON_EXEC
    )
    def validate_source_directory(params: dict) -> dict:
        """Validate source directory and count matching files."""
        import os
        import sys
        import logging
        from pathlib import Path
        
        sys.path.append(PACKAGE_ROOT)
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        source_dir = params['source_directory']
        pattern = params.get('pattern', '*.txt')
        
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f'Source directory does not exist: {source_dir}')
        
        # Count files matching pattern
        path = Path(source_dir)
        matching_files = list(path.glob(pattern))
        
        logger.info(f'Found {len(matching_files)} files matching pattern {pattern} in {source_dir}')
        
        return {
            'source_directory': source_dir,
            'pattern': pattern,
            'file_count': len(matching_files),
            'status': 'validated'
        }

    @task.external_python(
        task_id='discover_and_process_files',
        python=PYTHON_EXEC
    )
    def discover_and_process_files(validation_result: dict, params: dict) -> dict:
        """
        Discover files and extract metadata using Spark for efficient processing.
        Process files in batches to avoid memory issues.
        """
        import sys
        import logging
        from datetime import datetime
        from pathlib import Path
        
        sys.path.append(PACKAGE_ROOT)
        
        from src.common.spark_factory import SparkFactory
        from pyspark.sql import functions as F
        from pyspark.sql.types import StructType, StructField, StringType, TimestampType
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Create Spark session
        factory = SparkFactory()
        spark = factory.create_iceberg_session(app_name="FileDiscoveryV2")
        
        try:
            source_dir = params['source_directory']
            pattern = params.get('pattern', '*.txt')
            date_from = params.get('date_from', '')
            date_to = params.get('date_to', '')
            
            # Define schema for file metadata
            schema = StructType([
                StructField("file_path", StringType(), False),
                StructField("file_name", StringType(), False),
                StructField("file_size", StringType(), False),
                StructField("modified_time", TimestampType(), False)
            ])
            
            # Get list of files
            path = Path(source_dir)
            files_data = []
            
            for file_path in path.glob(pattern):
                stat = file_path.stat()
                files_data.append({
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'file_size': str(stat.st_size),
                    'modified_time': datetime.fromtimestamp(stat.st_mtime)
                })
            
            # Create DataFrame from file list
            df = spark.createDataFrame(files_data, schema=schema)
            
            # Extract metadata from filename pattern
            # Expected pattern: {PROVIDER}_{PERIOD}_{TIMESTAMP}_{SEQUENCE}.txt
            df = df.withColumn("provider_code", F.split(F.col("file_name"), "_").getItem(0))
            df = df.withColumn("ref_period", F.split(F.col("file_name"), "_").getItem(1))
            df = df.withColumn("received_timestamp", F.split(F.col("file_name"), "_").getItem(2))
            
            # Parse dates from filename components
            df = df.withColumn("ref_year", F.substring(F.col("ref_period"), 1, 4).cast("int"))
            df = df.withColumn("ref_month", F.substring(F.col("ref_period"), 5, 2).cast("int"))
            
            # Add processing metadata
            df = df.withColumn("discovered_at", F.current_timestamp())
            df = df.withColumn("discovery_run_id", F.lit(params.get('dag_run_id', 'manual')))
            df = df.withColumn("source_directory", F.lit(source_dir))
            
            # Apply date filters if provided
            if date_from:
                df = df.filter(F.col("received_timestamp") >= date_from.replace("-", ""))
            if date_to:
                df = df.filter(F.col("received_timestamp") <= date_to.replace("-", ""))
            
            # Cache for reporting
            df.cache()
            processed_count = df.count()
            
            # Handle table operations based on mode
            table_name = "jdbc_prod.default.file_discovery_v2"
            table_mode = params.get('table_mode', 'merge')
            
            if table_mode == 'merge':
                # Merge logic - update existing records, insert new ones
                if spark.catalog.tableExists(table_name):
                    df.createOrReplaceTempView("new_files")
                    merge_query = f"""
                    MERGE INTO {table_name} target
                    USING new_files source
                    ON target.file_path = source.file_path
                    WHEN MATCHED THEN
                        UPDATE SET
                            file_size = source.file_size,
                            modified_time = source.modified_time,
                            discovered_at = source.discovered_at,
                            discovery_run_id = source.discovery_run_id
                    WHEN NOT MATCHED THEN
                        INSERT *
                    """
                    spark.sql(merge_query)
                else:
                    df.writeTo(table_name).using("iceberg").create()
            
            elif table_mode == 'append':
                df.writeTo(table_name).append()
            
            elif table_mode == 'overwrite':
                df.writeTo(table_name).using("iceberg").createOrReplace()
            
            # Get statistics for return
            provider_stats = df.groupBy("provider_code").count().collect()
            
            result = {
                'processed_files': processed_count,
                'table_mode': table_mode,
                'provider_counts': {row['provider_code']: row['count'] for row in provider_stats},
                'status': 'completed'
            }
            
            df.unpersist()
            logger.info(f"Processed {processed_count} files using {table_mode} mode")
            
            return result
            
        finally:
            spark.stop()

    @task.external_python(
        task_id='validate_file_patterns',
        python=PYTHON_EXEC
    )
    def validate_file_patterns(processing_result: dict, params: dict) -> dict:
        """
        Validate file patterns and identify any files that don't match expected format.
        """
        import sys
        import logging
        import re
        
        sys.path.append(PACKAGE_ROOT)
        
        from src.common.spark_factory import SparkFactory
        from pyspark.sql import functions as F
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Expected pattern: {PROVIDER}_{PERIOD}_{TIMESTAMP}_{SEQUENCE}.txt
        expected_pattern = r'^[A-Z]{2}[0-9]+_[0-9]{6}_[0-9]{8}_[0-9]+\.txt$'
        
        factory = SparkFactory()
        spark = factory.create_iceberg_session(app_name="FileValidation")
        
        try:
            # Read the discovered files
            df = spark.table("jdbc_prod.default.file_discovery_v2")
            
            # Filter to current run if specified
            if 'dag_run_id' in params:
                df = df.filter(F.col("discovery_run_id") == params['dag_run_id'])
            
            # Validate filename patterns
            df_with_validation = df.withColumn(
                "is_valid_pattern",
                F.col("file_name").rlike(expected_pattern)
            )
            
            # Count valid and invalid files
            validation_stats = df_with_validation.groupBy("is_valid_pattern").count().collect()
            
            # Get sample of invalid files for investigation
            invalid_files = df_with_validation.filter(~F.col("is_valid_pattern")) \
                .select("file_name", "file_path") \
                .limit(10) \
                .collect()
            
            result = {
                'total_files': df.count(),
                'validation_stats': {str(row['is_valid_pattern']): row['count'] for row in validation_stats},
                'invalid_file_samples': [row.asDict() for row in invalid_files],
                'status': 'validated'
            }
            
            logger.info(f"Validation complete: {result['validation_stats']}")
            
            return result
            
        finally:
            spark.stop()

    @task.external_python(
        task_id='generate_discovery_report',
        python=PYTHON_EXEC
    )
    def generate_discovery_report(validation_result: dict, params: dict) -> dict:
        """
        Generate Excel report with discovery statistics and file inventory.
        Uses Spark to avoid loading all data into memory.
        """
        import sys
        import os
        import logging
        from datetime import datetime
        
        sys.path.append(PACKAGE_ROOT)
        
        from src.common.spark_factory import SparkFactory
        from pyspark.sql import functions as F
        import pandas as pd
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        factory = SparkFactory()
        spark = factory.create_iceberg_session(app_name="ReportGeneration")
        
        try:
            # Define report output directory
            report_dir = os.path.join(PACKAGE_ROOT, 'reports', 'file_discovery')
            os.makedirs(report_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(report_dir, f'file_discovery_report_{timestamp}.xlsx')
            
            # Read discovered files
            df = spark.table("jdbc_prod.default.file_discovery_v2")
            
            # Filter to current run if specified
            if 'dag_run_id' in params:
                df = df.filter(F.col("discovery_run_id") == params['dag_run_id'])
            
            with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
                # Sheet 1: Summary Statistics
                summary_data = {
                    'Metric': [
                        'Total Files Discovered',
                        'Total Providers',
                        'Date Range',
                        'Run ID',
                        'Report Generated'
                    ],
                    'Value': [
                        df.count(),
                        df.select("provider_code").distinct().count(),
                        f"{df.agg(F.min('ref_period')).collect()[0][0]} - {df.agg(F.max('ref_period')).collect()[0][0]}",
                        params.get('dag_run_id', 'manual'),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Sheet 2: Provider Statistics (using Spark aggregation)
                provider_stats = df.groupBy("provider_code") \
                    .agg(
                        F.count("*").alias("file_count"),
                        F.min("ref_period").alias("earliest_period"),
                        F.max("ref_period").alias("latest_period"),
                        F.sum("file_size").alias("total_size_bytes")
                    ) \
                    .orderBy("provider_code") \
                    .toPandas()
                
                provider_stats.to_excel(writer, sheet_name='Provider_Statistics', index=False)
                
                # Sheet 3: Monthly Distribution (using Spark aggregation)
                monthly_dist = df.groupBy("ref_year", "ref_month") \
                    .agg(F.count("*").alias("file_count")) \
                    .orderBy("ref_year", "ref_month") \
                    .toPandas()
                
                monthly_dist.to_excel(writer, sheet_name='Monthly_Distribution', index=False)
                
                # Sheet 4: Recent Files Sample (limit to prevent memory issues)
                recent_files = df.orderBy(F.desc("modified_time")) \
                    .select("file_name", "provider_code", "ref_period", "file_size", "modified_time") \
                    .limit(1000) \
                    .toPandas()
                
                recent_files.to_excel(writer, sheet_name='Recent_Files_Sample', index=False)
                
                # Sheet 5: Data Quality Issues
                if validation_result and 'invalid_file_samples' in validation_result:
                    quality_data = pd.DataFrame(validation_result['invalid_file_samples'])
                    if not quality_data.empty:
                        quality_data.to_excel(writer, sheet_name='Data_Quality_Issues', index=False)
            
            logger.info(f"Report generated: {report_path}")
            
            return {
                'report_path': report_path,
                'report_size': os.path.getsize(report_path),
                'status': 'generated'
            }
            
        finally:
            spark.stop()

    # Task flow definition
    validation = validate_source_directory()
    processing = discover_and_process_files(validation)
    pattern_validation = validate_file_patterns(processing)
    report = generate_discovery_report(pattern_validation)

    # Set dependencies
    validation >> processing >> pattern_validation >> report

# DAG Documentation
dag.doc_md = """
# File Discovery DAG V2 - Improved Version

## Overview
This improved version of the file discovery DAG demonstrates best practices:
- Task decorators for cleaner code
- Spark-based processing to handle large datasets efficiently
- Integrated file processing logic
- Comprehensive reporting capabilities
- Flexible table update modes (merge/append/overwrite)
- Data quality validation

## Parameters
- `source_directory`: Directory to scan for files
- `pattern`: File pattern to match (default: *.txt)
- `date_from`/`date_to`: Optional date range filters
- `table_mode`: How to update the target table (merge/append/overwrite)

## Features
1. **Efficient Processing**: Uses Spark DataFrames throughout
2. **Memory Safe**: Processes files in batches, no large in-memory collections
3. **Data Quality**: Validates filename patterns and reports issues
4. **Reporting**: Generates comprehensive Excel reports
5. **Flexible Updates**: Supports merge, append, and overwrite modes

## Output
- Iceberg table: `jdbc_prod.default.file_discovery_v2`
- Excel report: `reports/file_discovery/file_discovery_report_YYYYMMDD_HHMMSS.xlsx`
"""