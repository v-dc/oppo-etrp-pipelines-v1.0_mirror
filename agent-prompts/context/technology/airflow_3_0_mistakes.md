# Airflow 3.0 Common Mistakes

---
title: Airflow 3.0 Common Mistakes and Prevention
purpose: Help Claude Code avoid frequent errors when using Airflow 3.0
audience: [claude-code]
created: 2025-07-07
version: 1.0
related_files: [context/technology/airflow_3.0_syntax.md]
---

## Purpose
Document common mistakes when using Airflow 3.0 and provide solutions.

## Summary
This guide addresses the most frequent errors encountered during CB-Core development with Airflow 3.0, particularly focusing on syntax changes, virtual environment integration, and CB-Core specific patterns.

## Critical Mistakes

### 1. Schedule Parameter: Using Deprecated schedule_interval

**Problem**: Using `schedule_interval` parameter causes DAG parsing failures in Airflow 3.0
**Symptoms**: DAG parsing errors, DAG not appearing in web interface
- Error message: "Unexpected keyword argument 'schedule_interval'"
- DAG shows as broken or missing in Airflow UI

**Root Cause**: Airflow 3.0 deprecated `schedule_interval` in favor of `schedule`

**Solution**: Always use `schedule` parameter
```python
# ❌ Wrong approach that causes the mistake
dag = DAG(
    'dag_name',
    schedule_interval='@daily',  # DEPRECATED - Will cause errors
)

# ✅ Correct approach  
dag = DAG(
    'dag_name',
    schedule='@daily',  # Use 'schedule' parameter
)
```

**Prevention**: Always use `schedule` parameter in DAG definitions
- Code review checklist: Verify no `schedule_interval` usage
- Automated checks: Search for `schedule_interval` in DAG files
- Pattern to follow: Use CB-Core DAG template

### 2. Virtual Environment: Not Using @task.external_python for CB-Core

**Problem**: Using standard @task decorator instead of @task.external_python for CB-Core virtual environment
**Symptoms**: Import errors, package not found errors, using wrong Python interpreter
- ModuleNotFoundError for CB-Core modules
- Tasks using Airflow's Python instead of CB-Core's Python
- Missing CB-Core specific packages and configurations

**Root Cause**: Standard @task runs in Airflow's environment, not CB-Core's virtual environment

**Solution**: Use @task.external_python with CB-Core Python path
```python
# ❌ Wrong approach that causes the mistake
@task
def cb_core_processing():
    # This runs in Airflow's environment, not CB-Core venv
    from src.common.spark_factory import CBSparkSessionFactory  # Import error!
    return process_data()

# ✅ Correct approach  
CB_CORE_PYTHON = "/data1/systems/cb-system/venvs-cb/cb3.12/bin/python"

@task.external_python(
    python=CB_CORE_PYTHON,
    expect_airflow=False  # CB-Core venv doesn't include Airflow
)
def cb_core_processing():
    """
    All imports must be inside the function.
    """
    import sys
    sys.path.append('/data1/systems/cb-system/cb-core/src')
    
    from common.spark_factory import CBSparkSessionFactory
    
    # CB-Core processing logic
    spark = CBSparkSessionFactory.create_historical_session("CB-Core-Task")
    try:
        result = {"status": "success"}
        return result
    finally:
        spark.stop()
```

**Prevention**: Always use @task.external_python for CB-Core operations
- Code review checklist: Verify external Python usage for CB-Core tasks
- Pattern to follow: @task.external_python with CB-Core Python path
- Import strategy: All imports inside function body

### 3. TaskFlow API: Incorrect Import Strategy in External Python

**Problem**: Importing modules at file level instead of inside the function for external Python tasks
**Symptoms**: Import errors when using @task.external_python
- Module import failures in external Python environment
- "Module not found" errors despite correct virtual environment
- Tasks fail at startup before function execution

**Root Cause**: External Python environment doesn't have access to file-level imports

**Solution**: Move all imports inside the function body
```python
# ❌ Wrong approach that causes the mistake
from common.spark_factory import CBSparkSessionFactory  # File-level import fails

@task.external_python(python=CB_CORE_PYTHON, expect_airflow=False)
def cb_core_task():
    # CBSparkSessionFactory not available here
    spark = CBSparkSessionFactory.create_session("test")

# ✅ Correct approach  
@task.external_python(python=CB_CORE_PYTHON, expect_airflow=False)
def cb_core_task():
    """
    All imports must be inside the function for external Python.
    """
    import sys
    sys.path.append('/data1/systems/cb-system/cb-core/src')
    
    # Import CB-Core modules inside function
    from common.spark_factory import CBSparkSessionFactory
    
    spark = CBSparkSessionFactory.create_session("test")
    # ... processing logic
```

**Prevention**: Always import inside external Python functions
- Code review checklist: Verify no file-level imports for external Python tasks
- Pattern to follow: sys.path.append() + imports inside function
- Documentation: All external Python functions must be self-contained

### 4. TaskFlow Dependencies: Mixing TaskFlow with Traditional Operators Incorrectly

**Problem**: Incorrect dependency definition when mixing @task decorators with traditional operators
**Symptoms**: Dependencies not working as expected, execution order issues
- Tasks run in wrong order
- Data not passed correctly between TaskFlow and traditional operators
- Dependency graph appears broken in UI

**Root Cause**: TaskFlow uses different dependency patterns than traditional operators

**Solution**: Use proper dependency syntax for mixed approaches
```python
# ❌ Wrong approach that causes the mistake
@task
def extract_data():
    return {"data": "extracted"}

bash_task = BashOperator(task_id='process_bash', bash_command='echo "processing"')

# Wrong: TaskFlow function doesn't establish dependency
extract_data() >> bash_task  # This won't work as expected

# ✅ Correct approach  
@task
def extract_data():
    return {"data": "extracted"}

bash_task = BashOperator(task_id='process_bash', bash_command='echo "processing"')

# Correct: Assign TaskFlow result to variable, then set dependency
extracted_task = extract_data()
extracted_task >> bash_task
```

**Prevention**: Understand TaskFlow vs traditional operator dependency patterns
- Code review checklist: Verify correct dependency syntax for mixed approaches
- Pattern to follow: Assign TaskFlow tasks to variables before setting dependencies
- Testing: Verify execution order in Airflow UI

### 5. File Paths: Using Generic Paths Instead of CB-Core Specific

**Problem**: Using generic or incorrect file paths for CB-Core integration
**Symptoms**: File not found errors, incorrect data processing
- Tasks fail with path-related errors
- Data processing operates on wrong directories
- External Python tasks cannot find CB-Core modules

**Root Cause**: Not following CB-Core directory structure and conventions

**Solution**: Use CB-Core specific file paths and sys.path configuration
```python
# ❌ Wrong approach that causes the mistake
@task.external_python(python="/usr/bin/python3")  # Wrong Python
def process_data():
    from src.common import utils  # Wrong path, won't find CB-Core modules

# ✅ Correct approach  
CB_CORE_PYTHON = "/data1/systems/cb-system/venvs-cb/cb3.12/bin/python"

@task.external_python(python=CB_CORE_PYTHON, expect_airflow=False)
def process_data():
    import sys
    sys.path.append('/data1/systems/cb-system/cb-core/src')  # CB-Core source path
    
    from common import utils  # Now can find CB-Core modules
```

**Prevention**: Always use CB-Core standard paths and Python environment
- Code review checklist: Verify CB-Core Python path and sys.path setup
- Pattern to follow: CB-Core Python binary + sys.path configuration
- Testing: Verify module imports work in external Python environment

## Warning Signs

Watch for these indicators that suggest mistakes:
- **DAG parsing errors**: Usually indicates syntax or import issues (check for `schedule_interval`)
- **TaskFlow dependency issues**: Tasks not running in expected order (check dependency syntax)
- **Virtual environment errors**: ImportError or ModuleNotFoundError for CB-Core modules (use @task.external_python)
- **File not found errors**: Suggests incorrect path usage or missing sys.path setup
- **External Python failures**: Function-level import errors (move imports inside function)
- **Service control failures**: Indicates outdated service name usage

## Quick Reference

### Before You Code Checklist
- [ ] Use `schedule` parameter (not `schedule_interval`)
- [ ] Use @task.external_python for CB-Core virtual environment
- [ ] Import all modules inside external Python functions
- [ ] Use CB-Core specific Python path: `/data1/systems/cb-system/venvs-cb/cb3.12/bin/python`
- [ ] Set expect_airflow=False for CB-Core external Python tasks
- [ ] Include CB-Core tags in DAG definition

### Code Review Checklist  
- [ ] No `schedule_interval` usage anywhere
- [ ] @task.external_python used for CB-Core operations
- [ ] All imports inside external Python function bodies
- [ ] sys.path.append() for CB-Core source path
- [ ] Proper TaskFlow dependency syntax for mixed approaches
- [ ] CB-Core naming conventions applied

## Related Patterns

These CB-Core patterns help avoid mistakes:
- `examples/airflow_dag_template.py` - Prevents syntax and structure mistakes  
- `standards/core_development_patterns.md` - Prevents naming and convention mistakes
- `context/technology/airflow_3.0_syntax.md` - Reference for correct TaskFlow usage

## Emergency Fixes

### If You Encounter DAG Parsing Errors:
1. **Step 1**: Check for `schedule_interval` usage and replace with `schedule`
2. **Step 2**: Verify all imports are Airflow 3.0 compatible
3. **Step 3**: Validate DAG syntax with `airflow dags list`

### If You Encounter TaskFlow Import Issues:
1. **Step 1**: Move all imports inside the @task.external_python function
2. **Step 2**: Add sys.path.append('/data1/systems/cb-system/cb-core/src')
3. **Step 3**: Test imports manually in CB-Core virtual environment

### If You Encounter Virtual Environment Issues:
1. **Step 1**: Replace @task with @task.external_python for CB-Core operations
2. **Step 2**: Use CB-Core Python path: `/data1/systems/cb-system/venvs-cb/cb3.12/bin/python`
3. **Step 3**: Set expect_airflow=False parameter

### If You Encounter Dependency Issues:
1. **Step 1**: Assign TaskFlow tasks to variables before setting dependencies
2. **Step 2**: Use proper >> operator syntax with task variables
3. **Step 3**: Verify dependency graph in Airflow UI