# TASK: Historical File Discovery & Metadata Table Creation

Create file discovery system that scans historical files and populates an Iceberg metadata table, orchestrated by an Airflow DAG.

## DELIVERABLES
- **Discovery Module**: `src/discovery/historical_file_discovery.py` - Core file scanning and metadata extraction
- **Iceberg Schema**: `sql/ddl/create_file_metadata_table.sql` - Iceberg table definition  
- **Airflow DAG**: `airflow/dags/historical_processing/file_discovery_dag.py` - Manual trigger orchestration
- **Unit Tests**: `tests/unit/test_file_discovery.py` - Comprehensive validation

## SUCCESS CRITERIA
- [ ] Discover and parse all files in historical directory
- [ ] Extract metadata from filename pattern correctly
- [ ] Create/update Iceberg table with file inventory
- [ ] Support incremental discovery runs
- [ ] Comprehensive error handling and logging
- [ ] Manual Airflow trigger with configurable parameters

## CONTEXT FILES
- **Airflow Syntax**: `agent-prompts/context/airflow3_syntax_guide.md` - Airflow 3.0 patterns
- **Development Patterns**: `agent-prompts/context/cb_core_development_patterns.md` - CB-Core conventions
- **Schema Reference**: `agent-prompts/schemas/credit_bureau_schema.yaml` - Data structure
- **Spark Factory**: `src/common/spark_factory.py` - Session creation patterns

## TECHNICAL SPECIFICATIONS

### Iceberg Table Requirements
- **Table**: `jdbc_prod.default.cb_file_metadata`
- **Schema**: filename, provider_code, reference_period, received_date, received_datetime, file_size, file_path, discovery_timestamp
- **Partitioning**: By provider_type (BK/MG/LN/FS/OT) and reference_year
- **Operation**: CREATE OR REPLACE for idempotency

### Processing Requirements
- **Source**: `/data1/systems/cb-system/data/raw/` (19,976 files)
- **Filename Pattern**: `{PROVIDER}_{PERIOD}_{TIMESTAMP}_{SEQUENCE}.txt`
- **Universal Priority**: Sort by ref_period → received → provider
- **Error Handling**: Skip invalid files, log all issues
- **Performance**: Process in batches, support configurable date ranges

### Airflow DAG Requirements
- **Name**: `cb_historical_file_discovery`
- **Trigger**: Manual only (`schedule=None`)
- **Mode**: Exclusive processing (pause live DAGs when active)
- **Configuration**: Support date range parameters
- **Resource**: Use historical Spark profile (maximum allocation)

## IMPLEMENTATION STANDARDS
- Use CB-Core standards for error handling, logging with correlation IDs, and resource cleanup
- Follow Airflow 3.0 syntax exactly as specified in context files
- Apply CB-Core naming conventions and development patterns
- Include comprehensive unit tests with pytest fixtures
- Support configurable parameters for flexible operation