# Credit Bureau Template - Recasted Solution Architecture v1.0

## Project Overview

**Goal**: Create a production-ready credit bureau data platform template for rapid client deployment, processing 19,976 historical files (1999-2024) and ongoing monthly data feeds from financial institutions.

**Timeline**: 1-week development sprint using AI-agentic development with Claude Code
**Environment**: NPD Server (Intel Xeon E-2378, 8 cores, 32GB RAM)

## System Architecture - NPD Server Integration

### Core File System Layout
```
/opt/airflow/                         [Airflow Installation]
├── airflow.cfg                       [Airflow configuration file] 
├── dags/                             [Airflow DAGs directory - CB DAGs via bundle]
├── logs/                             [Airflow execution logs]
└── venv/                             [Airflow Python virtual environment]

/data1/systems/cb-system/             [Main CB-System Directory]
├── cb-app/                           [Frontend Application]
├── cb-core/                          [GIT REPOSITORY - Our Development Focus]
├── config/                           [System Configuration Files]
├── data/                             [Dedicated to CB-System]
│   ├── raw/                          [HISTORICAL DATA - 19,976 files]
│   ├── raw-incoming/                 [LIVE INCOMING DATA - Proposed]
│   └── processed/                    [PROCESSED FILE ARCHIVE]
├── docker/                           [Docker configurations]
├── drivers/                          [Database drivers (JDBC, etc.)]
├── logs/                             [Application logs]
├── tests/                            [Test scripts and validation]
└── venvs-cb/                         [VIRTUAL ENVIRONMENTS]

/data2/systems/data/                  [Data Storage Layer]
├── db-replicas/                      [Database backup replicas]
├── jdbc_warehouse/                   [ICEBERG WAREHOUSE FOR STAGING]
│   └── default/                      [Default namespace tables]
└── raw-storage/                      [EXTERNAL TO CB SYSTEM]
    ├── data_sample/                  [Sample datasets]
    └── fdmac/                        [FDMAC data source]
```

### CB-Core Repository Structure
```
/data1/systems/cb-system/cb-core/     [GIT REPOSITORY]
├── agent-prompts/                    [Claude Code Framework]
│   ├── tasks/                        [Module task specifications]
│   │   ├── ingestion/               [S3/file ingestion tasks]
│   │   ├── transformation/          [Data transformation tasks]
│   │   ├── validation/              [Quality validation tasks]
│   │   └── orchestration/           [DAG orchestration tasks]
│   ├── schemas/                      [Data schema definitions]
│   ├── standards/                    [Coding and operational standards]
│   ├── examples/                     [Templates and reference patterns]
│   └── executed_prompts/             [Prompt execution audit trail]
├── airflow/                          [Airflow Integration]
│   ├── dags/                         [CB-Core DAG definitions]
│   │   ├── live_processing/         [Live data processing DAGs]
│   │   ├── historical_processing/   [Historical data processing DAGs]
│   │   └── common/                  [Shared DAG components]
│   └── plugins/                      [Custom Airflow operators]
├── src/                              [Python Source Code]
│   ├── common/                       [Shared utilities and patterns]
│   ├── ingestion/                    [Data ingestion modules]
│   ├── transformation/               [Data transformation modules]
│   ├── validation/                   [Data quality and validation]
│   ├── quality/                      [Great Expectations integration]
│   └── orchestration/               [Workflow orchestration helpers]
├── spark/                            [Spark Configurations]
│   └── configs/                      [Environment-specific configs]
├── great_expectations/               [Data Quality Framework]
│   ├── expectations/                 [Data validation rules]
│   ├── checkpoints/                  [Validation checkpoints]
│   └── datasources/                  [Data source configurations]
├── sql/                              [SQL Scripts]
│   ├── ddl/                          [Table creation scripts]
│   ├── dml/                          [Data manipulation scripts]
│   └── migrations/                   [Schema migration scripts]
├── tests/                            [Testing Framework]
│   ├── unit/                         [Unit tests]
│   ├── integration/                  [Integration tests]
│   └── fixtures/                     [Test data fixtures]
├── scripts/                          [Automation Scripts]
│   ├── deployment/                   [Deployment automation]
│   ├── monitoring/                   [Monitoring and alerting]
│   └── operations/                   [Operational maintenance]
├── docs/                             [Documentation]
│   ├── api/                          [API documentation]
│   ├── operations/                   [Operational guides]
│   └── deployment/                   [Deployment instructions]
└── .github/workflows/                [CI/CD Pipeline]
```

## Technology Stack - Confirmed Integration

### Infrastructure
- **Server**: NPD Server (Dell PowerEdge T150, 8 cores, 32GB RAM)
- **Storage**: 960GB SSD + 2×2TB HDD
- **Network**: Internal network (192.168.0.74)

### Core Technologies - Pre-Configured
- **Apache Airflow 3.0**: ✅ Running at `/opt/airflow/`
- **Apache Spark 3.5.6**: ✅ Installed, optimized for single-node
- **PostgreSQL 16**: ✅ Configured with `jdbc_catalog_db` and `boards` databases
- **Apache Iceberg**: ✅ JDBC catalog configured at `/data2/systems/data/jdbc_warehouse/`
- **Python 3.9+**: ✅ Ready for development

### Database Configuration - Validated
```python
# Iceberg Catalog (Staging Data)
spark = SparkSession.builder \
    .config("spark.sql.catalog.jdbc_prod", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.jdbc_prod.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog") \
    .config("spark.sql.catalog.jdbc_prod.uri", "jdbc:postgresql://localhost:5432/jdbc_catalog_db") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.user", "jdbc_user") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.password", "jdbc_password") \
    .config("spark.sql.catalog.jdbc_prod.warehouse", "/data2/systems/data/jdbc_warehouse") \
    .getOrCreate()

# Operational Database (Analytics Tables)
jdbc_url = "jdbc:postgresql://192.168.0.74:5432/boards"
connection_properties = {
    "user": "spark_user",
    "password": "spark_password",
    "driver": "org.postgresql.Driver"
}
```

## Exclusive Processing Architecture

### Live Processing System (Default Active)
- **Data Source**: `/data1/systems/cb-system/data/raw-incoming/` (proposed)
- **Processing**: Real-time file processing as files arrive
- **Resource Allocation**: Up to 2 Spark jobs (6 cores, 20GB memory)
- **Priority**: Universal priority (ref_period → received → provider)

### Historical Processing System (Manual Activation)
- **Data Source**: `/data1/systems/cb-system/data/raw/` (19,976 existing files)
- **Processing**: Batch processing with configurable date ranges
- **Resource Allocation**: Same 2 Spark jobs (exclusive operation)
- **Activation**: Manual trigger, completely deactivates live system

### Exclusive Operation Rules
1. **Never Concurrent**: Only Live OR Historical active, never both
2. **Complete Deactivation**: Inactive system fully stopped
3. **Resource Sharing**: Same infrastructure used exclusively
4. **File Accumulation**: Live files accumulate during historical processing

## Data Flow Architecture

### Universal Data Processing Pipeline
```
Input Files → Spark Processing → Great Expectations Validation → 
Iceberg Staging (All Data + Quality Flags) → Manual Corrections → 
Great Expectations Re-run → PostgreSQL Operational (Clean Data Only)
```

### Data Storage Strategy
- **Iceberg Warehouse**: Complete data staging with quality metadata
- **PostgreSQL `boards`**: Clean operational data for analytics/Metabase
- **File Archive**: Processed files moved to `/data1/systems/cb-system/data/processed/`

## Development Workflow - AI-Agentic Approach

### Task-Driven Development
1. **Task Definition**: Create detailed specifications in `agent-prompts/tasks/`
2. **Claude Code Execution**: Use explicit context pattern for development
3. **Quality Assurance**: Automated testing and validation
4. **Documentation**: Comprehensive audit trail in `executed_prompts/`

### Example Development Command
```bash
claude-code "Create S3 ingestion pipeline as defined in agent-prompts/tasks/ingestion/file_processing.md. 
Use schemas/credit_bureau_schema.yaml and follow standards/error_handling.md"
```

### Prompt Documentation Pattern
```markdown
# agent-prompts/executed_prompts/YYYY-MM-DD_feature_version.md
## Metadata
- Timestamp: YYYY-MM-DD HH:MM:SS
- Developer: [Name]
- Task Reference: tasks/[module]/[feature].md

## PROMPT
[Exact prompt used]

## OUTCOME
- Generated: [files created]
- Status: SUCCESS/PARTIAL/FAILED
- Notes: [observations]
```

## Credit Bureau Data Characteristics

### Historical Data Inventory
- **Total Files**: 19,976 files (February 1999 - December 2024)
- **Institution Types**: 123 institutions across 5 categories (BK, MG, LN, FS, OT)
- **File Format**: 63-field pipe-delimited text files
- **Data Integration**: Combined origination + servicing data per record

### File Format Structure
- **Origination Fields**: Positions 1-31 (loan application details)
- **Servicing Fields**: Positions 32-63 (monthly performance data)
- **Business Key**: `id_loan` + `period` (unique identifier)
- **Quality Pattern**: High completeness on core fields, sparse on optional fields

### Data Quality Framework
- **Initial Validation**: Great Expectations on raw ingestion
- **Staging Strategy**: All data loaded with quality flags
- **Manual Corrections**: Applied in Iceberg staging layer
- **Re-validation**: Quality scores updated after corrections
- **Operational Load**: Only clean, validated data to PostgreSQL

## Resource Optimization - NPD Server

### Spark Configuration (Optimized)
```yaml
spark_config:
  driver_memory: "4g"
  driver_cores: 1
  executor_instances: 2
  executor_cores: 3
  executor_memory: "8g"
  executor_memory_overhead: "2g"
  
# Resource allocation:
# Cores: 1 (driver) + 6 (executors) = 7/8 cores used
# Memory: 4g (driver) + 20g (executors) = 24GB/32GB used
# Buffer: 1 core + 8GB for OS and development tools
```

### Processing Performance Targets
- **Historical Processing**: 100-500 files/hour (depends on file size)
- **Live Processing**: Real-time processing within 30 minutes of file arrival
- **Quality Validation**: < 5 minutes per file for standard validation
- **Data Loading**: Complete pipeline < 2 hours for daily batch

## Integration Points

### Airflow DAG Bundle Configuration
```python
# /opt/airflow/airflow.cfg modification
[core]
dags_folder = /opt/airflow/dags:/data1/systems/cb-system/cb-core/airflow/dags
```

### Development Environment Setup
- **Virtual Environment**: `/data1/systems/cb-system/venvs-cb/`
- **Python Packages**: PySpark, Great Expectations, psycopg2, pandas
- **IDE Integration**: VS Code with Claude extension for AI-assisted development

## Current Project Status

### Completed Phases ✅
- **Phase 1**: Discovery & Requirements (Business requirements, technical assessment, data profiling)
- **Phase 2**: Architecture & Design (Solution architecture, data models, system design)

### Current Phase 🔄
- **Phase 3**: Development Environment Setup
  - CB-Core repository initialization
  - Airflow DAG bundle configuration
  - Development tools and standards setup
  - Agent-prompts framework implementation

### Upcoming Phases ⏳
- **Phase 4**: Incremental Development (Historical processing, live processing, quality framework)
- **Phase 5**: Integration & Testing (End-to-end validation, performance testing)
- **Phase 6**: Deployment & Operations (Production readiness, monitoring)

## Risk Management

### Technical Risks
- **Resource Constraints**: Single server limitations (mitigated by exclusive processing)
- **Data Quality**: Unknown issues in historical files (mitigated by comprehensive validation)
- **Processing Time**: 19,976 files in 1-week timeline (mitigated by parallel processing)

### Operational Risks
- **Mode Switching**: Live/Historical system conflicts (mitigated by exclusive operation)
- **File Accumulation**: Live files during historical processing (mitigated by monitoring)
- **Data Loss**: File processing failures (mitigated by comprehensive error handling)

## Success Metrics

### Technical Success Criteria
- [ ] All 19,976 historical files processed successfully
- [ ] Live processing workflow operational and real-time
- [ ] Iceberg lakehouse populated and queryable
- [ ] PostgreSQL operational database responding with clean data
- [ ] Template deployable on fresh CB-Core environment

### Quality Metrics
- [ ] < 1% data processing failures
- [ ] Zero data loss during ingestion
- [ ] Comprehensive data quality scoring (0-100 scale)
- [ ] Complete audit trail of all processing

### Performance Metrics
- [ ] Historical processing: 8-24 hours total processing time
- [ ] Live processing: < 30 minutes per file
- [ ] Query performance: < 10 seconds for standard operational queries
- [ ] System availability: > 99% uptime during business hours

## Team Resources

### Development Team
- **Primary Developer**: Using Claude Code for accelerated development
- **Technical Lead**: Architecture oversight and quality assurance
- **Operations**: NPD server management and deployment support

### Development Tools
- **AI Assistant**: Claude Code for rapid development and code generation
- **Version Control**: Git repository at `/data1/systems/cb-system/cb-core/`
- **IDE**: VS Code with Claude integration
- **Testing**: pytest framework with comprehensive test coverage

---

**Architecture Version**: 1.0 (NPD Server Integration)  
**Target Environment**: NPD Server with CB-System Integration  
**Key Innovation**: Exclusive processing with real system integration  
**Replaces**: phase2_updated_solution_architecture.md