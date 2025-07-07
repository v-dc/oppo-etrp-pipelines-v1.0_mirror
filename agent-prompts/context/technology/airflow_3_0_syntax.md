# Airflow 3.0 Syntax

---
title: Airflow 3.0 Syntax Guide for Claude Code
purpose: Guide Claude Code to use Airflow 3.0 correctly and avoid deprecated syntax
audience: [claude-code]
created: 2025-07-07
updated: 2025-07-07
version: 1.0
related_files: [context/technology/airflow_3.0_mistakes.md, examples/airflow_dag_template.py]
---

## Purpose
Guide Claude Code to use Airflow 3.0 correctly and avoid deprecated syntax from Airflow 2.x.

## Summary
Airflow 3.0 introduces critical syntax changes that break compatibility with 2.x. The most important change is using `schedule` instead of `schedule_interval`, along with updated service names and improved operator imports.

## Key Changes from Previous Version
- **schedule Parameter**: `schedule_interval` deprecated, use `schedule`
- **Service Names**: New service architecture with `airflow-dag-processor` and `airflow-api-server`
- **Import Updates**: Some operator imports have changed paths
- **Configuration Structure**: Improved default argument patterns

## Best Practices

### Modern TaskFlow API with @task Decorator
Use @task decorator for cleaner, more Pythonic DAG development.

**Example**:
```python
from airflow.sdk import dag, task
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=['cb-core', 'module'],
)
def cb_core_module_dag():
    """CB-Core module processing with TaskFlow API"""
    
    @task
    def extract_data():
        """Extract data from source"""
        # Your extraction logic
        return {"data": "extracted"}
    
    @task
    def transform_data(data: dict):
        """Transform extracted data"""
        # Your transformation logic
        return {"transformed": data["data"]}
    
    @task
    def load_data(data: dict):
        """Load transformed data"""
        # Your loading logic
        print(f"Loading: {data}")
    
    # TaskFlow automatically infers dependencies
    extracted = extract_data()
    transformed = transform_data(extracted)
    load_data(transformed)

# Create the DAG
dag_instance = cb_core_module_dag()
```

### Using CB-Core Virtual Environment with @task.external_python
For CB-Core specific virtual environment isolation, use @task.external_python.

**Example**:
```python
from airflow.sdk import dag, task
import pendulum

CB_CORE_PYTHON = "/data1/systems/cb-system/venvs-cb/cb3.12/bin/python"

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=['cb-core', 'module'],
)
def cb_core_external_python_dag():
    """CB-Core DAG using external Python environment"""
    
    @task.external_python(
        python=CB_CORE_PYTHON,
        expect_airflow=False  # CB-Core venv doesn't need Airflow
    )
    def process_with_cb_core_env():
        """
        Process data using CB-Core virtual environment.
        All imports must be inside the function.
        """
        import sys
        import logging
        
        # CB-Core specific processing
        print(f"Running in CB-Core Python: {sys.executable}")
        
        # Your CB-Core processing logic here
        # Import CB-Core modules as needed
        return {"status": "success"}
    
    @task
    def validate_results(result: dict):
        """Validate processing results in main Airflow environment"""
        print(f"Results: {result}")
        return result["status"] == "success"
    
    # TaskFlow dependencies
    result = process_with_cb_core_env()
    validate_results(result)

# Create the DAG
dag_instance = cb_core_external_python_dag()
```

### Traditional DAG Definition Pattern (Alternative)
Use when mixing TaskFlow with traditional operators.

**Example**:
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

default_args = {
    'owner': 'cb-core',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cb_core_module_dag',
    default_args=default_args,
    description='CB-Core module processing',
    schedule=None,  # CRITICAL: Use 'schedule' not 'schedule_interval'
    catchup=False,
    tags=['cb-core', 'module'],
    is_paused_upon_creation=True,
)

# Mix TaskFlow with traditional operators
@task(dag=dag)
def process_data():
    return {"processed": True}

bash_task = BashOperator(
    task_id='run_script',
    bash_command='''
    source /data1/systems/cb-system/venvs-cb/cb3.12/bin/activate
    python /data1/systems/cb-system/cb-core/src/module/script.py
    ''',
    dag=dag,
)

# Dependencies
processed = process_data()
processed >> bash_task
```

### Schedule Parameter Usage
Always use `schedule` parameter with proper values.

**Example**:
```python
# Manual trigger (most CB-Core DAGs)
schedule=None

# Daily processing
schedule='@daily'

# Custom cron schedule
schedule='0 6 * * *'  # Daily at 6 AM

# Multiple times per day
schedule='0 */6 * * *'  # Every 6 hours
```

### Standard Operator Imports
Use current Airflow 3.0 import paths.

**Example**:
```python
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
```

### CB-Core Integration Pattern
Use @task.external_python for CB-Core virtual environment and BashOperator for complex scripts.

**Example**:
```python
# CB-Core virtual environment path
CB_CORE_PYTHON = "/data1/systems/cb-system/venvs-cb/cb3.12/bin/python"

# TaskFlow with external Python environment
@task.external_python(
    python=CB_CORE_PYTHON,
    expect_airflow=False  # CB-Core venv doesn't include Airflow
)
def cb_core_spark_job():
    """
    Spark job using CB-Core environment.
    All imports must be inside the function.
    """
    import sys
    sys.path.append('/data1/systems/cb-system/cb-core/src')
    
    from common.spark_factory import CBSparkSessionFactory
    
    # Create Spark session using CB-Core factory
    spark = CBSparkSessionFactory.create_historical_session("CB-Core-Task")
    
    try:
        # Your Spark processing logic
        df = spark.sql("SHOW TABLES IN jdbc_prod.default")
        df.show()
        result = {"tables": df.count()}
    finally:
        spark.stop()
    
    return result

# BashOperator for complex operations with virtual environment
bash_task = BashOperator(
    task_id='run_complex_script',
    bash_command='''
    # Activate CB-Core virtual environment
    source /data1/systems/cb-system/venvs-cb/cb3.12/bin/activate
    
    # Run Python script with arguments
    python /data1/systems/cb-system/cb-core/src/module/complex_job.py \\
        --source-dir {{ dag_run.conf.get("source_dir", "/default/path/") }} \\
        --log-level {{ dag_run.conf.get("log_level", "INFO") }}
    ''',
    dag=dag,
)
```

## CB-Core Integration
How Airflow 3.0 integrates with CB-Core framework patterns:

### TaskFlow API Benefits for CB-Core
- **Cleaner Code**: @task decorator reduces boilerplate compared to traditional operators
- **Automatic Dependencies**: TaskFlow infers dependencies from function calls
- **Data Passing**: Automatic XCom handling between tasks
- **Type Hints**: Better IDE support and code clarity

### Virtual Environment Strategy
- **@task.external_python**: Recommended for CB-Core virtual environment isolation
- **Path**: `/data1/systems/cb-system/venvs-cb/cb3.12/bin/python`
- **expect_airflow=False**: CB-Core venv doesn't need Airflow installation
- **Import Strategy**: All imports must be inside the function body

### DAG Organization Options
1. **Pure TaskFlow**: Use @dag decorator for modern, clean DAGs
2. **Mixed Approach**: Combine @task with traditional operators when needed
3. **Traditional**: Use DAG class when complex configuration is required

### CB-Core Specific Patterns
- **Spark Jobs**: Use @task.external_python with CB-Core Spark factory
- **File Processing**: Use BashOperator for complex multi-step operations
- **Data Validation**: Use @task for Great Expectations integration
- **Error Handling**: Leverage TaskFlow automatic retry and error propagation

## Performance Notes
Airflow 3.0 performance optimizations for CB-Core:
- **DAG Parsing**: Improved parsing speed with DAG bundles
- **Task Scheduling**: Better resource utilization with new scheduler
- **Virtual Environment**: More reliable isolation with explicit activation

## References
- Official Airflow 3.0 documentation
- CB-Core framework integration patterns
- examples/airflow_dag_template.py