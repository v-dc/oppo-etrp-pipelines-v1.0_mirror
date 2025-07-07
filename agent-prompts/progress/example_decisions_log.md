# Architecture Decisions - CB-Core

## 2025-01-25: Manual System Configuration
- **Decision**: No automated changes to system config files (airflow.cfg, postgres, etc.)
- **Reason**: Safety, user control, avoid breaking existing systems
- **Impact**: Manual setup required, clear instructions provided
- **Implementation**: .md instruction files in manual_config_instructions/

## 2025-01-25: Airflow 3.0 Specific Context
- **Decision**: Dedicated context files for Airflow 3.0 syntax and patterns
- **Reason**: Avoid Claude Code using outdated Airflow 2.x syntax
- **Impact**: More accurate code generation, fewer syntax errors
- **Implementation**: agent-prompts/context/airflow3_syntax_guide.md

## 2025-01-25: Exclusive Processing Mode
- **Decision**: Live OR Historical processing, never concurrent
- **Reason**: Single server resource constraints, simpler operation
- **Impact**: Manual mode switching required
- **Implementation**: DAG-level activation/deactivation

## 2025-01-25: Staging-First Data Quality
- **Decision**: All data goes to Iceberg staging, then PostgreSQL gets clean data only
- **Reason**: Allow manual corrections, complete audit trail
- **Impact**: Two-stage loading process, higher storage requirements

## 2025-01-25: AI-Agentic Development Framework
- **Decision**: Use agent-prompts structure for Claude Code development
- **Reason**: Accelerated development, consistent patterns
- **Impact**: All development follows task-driven approach

## 2025-06-26: BashOperator Over SparkSubmitOperator for Virtual Environments
- **Decision**: Use BashOperator with explicit virtual environment activation instead of SparkSubmitOperator
- **Reason**: SparkSubmitOperator has connection conflicts and unreliable virtual environment handling
- **Impact**: More reliable DAG execution, explicit control over Python environment
- **Implementation**: `source /data1/systems/cb-system/venvs-cb/cb3.12/bin/activate` in bash commands
- **Alternatives Considered**: SparkSubmitOperator with various connection configurations (all failed)
- **Future Action**: Revisit SparkSubmitOperator approach after further research on connection handling

## 2025-06-26: Explicit DataFrame Schemas for Spark Operations
- **Decision**: Always define explicit DataFrame schemas instead of relying on Spark's type inference
- **Reason**: Type inference fails with nullable fields and mixed data types
- **Impact**: More code but reliable DataFrame creation and Iceberg operations
- **Implementation**: StructType with StructField definitions for all DataFrames
- **Alternatives Considered**: Schema inference (failed), pandas DataFrame conversion

## 2025-06-26: CREATE OR REPLACE TABLE Strategy for Discovery Pipeline
- **Decision**: Use CREATE OR REPLACE TABLE for file metadata table instead of incremental updates
- **Reason**: Discovery table should reflect current state of raw directory, not historical states
- **Impact**: Clean slate each run, table accurately represents current file inventory
- **Implementation**: Iceberg table recreated on each discovery run
- **Alternatives Considered**: Incremental updates with MERGE only (would leave stale records)

## 2025-06-26: Filename Pattern Analysis Before Implementation
- **Decision**: Always analyze actual filename patterns in data before implementing parsing logic
- **Reason**: Documentation may be outdated or incomplete compared to actual data
- **Impact**: Prevents "all files invalid" scenarios, ensures accurate metadata extraction
- **Implementation**: Manual file listing and pattern analysis as first development step
- **Alternatives Considered**: Trusting specification documents (led to parsing failures)

## Template for New Decisions
## YYYY-MM-DD: [Decision Title]
- **Decision**: [What was decided]
- **Reason**: [Why this approach]
- **Impact**: [How it affects the project]
- **Implementation**: [How it's implemented]
- **Alternatives Considered**: [Other options evaluated]
