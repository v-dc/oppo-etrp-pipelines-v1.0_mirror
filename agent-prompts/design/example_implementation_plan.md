# Data Solution Delivery Process with Claude Integration

## Overview
A comprehensive process for delivering data solutions using Claude as a design partner and Claude Code for development, leveraging our core stack: Airflow, PySpark, Python, Great Expectations, Postgres, Iceberg (JDBC catalog), and Metabase.

## Phase 1: Discovery & Requirements

### 1.1 Business Requirements Analysis
- Capture business objectives and success criteria
- Define SLAs, data freshness requirements, and KPIs
- Identify stakeholders and data consumers
- Document data sources, volumes, velocity, and variety
- **With Claude:** Generate requirement templates, validate completeness, identify edge cases

### 1.2 Technical Assessment
- Evaluate existing infrastructure capacity
- Assess data source connectivity and access patterns
- Review security and compliance requirements
- Estimate costs and resource requirements
- **With Claude:** Create technical assessment checklists, analyze trade-offs

### 1.3 Data Profiling & Discovery
- Profile source data for quality issues
- Identify data types, distributions, and patterns
- Document business rules and transformations
- Map data lineage requirements
- **With Claude:** Generate profiling scripts, analyze findings, suggest quality rules

## Phase 2: Architecture & Design

### 2.1 Solution Architecture
- Design end-to-end data flow architecture
- Define component interactions and boundaries
- Plan for scalability and fault tolerance
- Design metadata and catalog strategy
- **With Claude:** Generate architecture diagrams (Mermaid), review patterns, validate design

### 2.2 Data Modeling
- Design dimensional/analytical models
- Define Iceberg table schemas and partitioning
- Plan slowly changing dimension strategies
- Design data quality framework
- **With Claude:** Generate DDL, optimize schemas, create naming conventions

### 2.3 Security & Compliance Design
- Define access control requirements
- Plan data encryption and masking
- Design audit logging strategy
- Document compliance requirements (GDPR, HIPAA, etc.)
- **With Claude:** Generate security policies, create compliance checklists

## Phase 3: Development Environment Setup

### 3.1 Project Structure
```
project-root/
├── agent-prompts/
│   ├── context.yaml                     # Project setup/solution decomposition
│   ├── tasks/                           # Module tasks in markdown
│   │   ├── ingestion/
│   │   ├── transformation/
│   │   └── validation/
│   ├── schemas/                         # Reusable schemas
│   │   ├── raw/
│   │   ├── staging/
│   │   └── analytics/
│   ├── standards/                       # Common patterns
│   │   ├── logging.md
│   │   ├── error_handling.md
│   │   └── spark_config.yaml
│   ├── examples/
│   │   ├── spark_job_template.py
│   │   └── dag_template.py
│   └── executed_prompts/                # Audit trail of prompts
│       ├── 2025-01-15_s3_ingestion_v1.md
│       └── prompt_log.yaml
├── airflow/
│   ├── dags/
│   │   ├── ingestion/
│   │   ├── transformation/
│   │   ├── orchestration/
│   │   └── common/
│   ├── plugins/
│   └── config/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   └── common/
├── spark/
│   └── configs/
├── great_expectations/
│   ├── expectations/
│   ├── checkpoints/
│   └── datasources/
├── sql/
│   ├── ddl/
│   ├── dml/
│   └── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── deployment/
│   └── monitoring/
├── docs/
└── .github/workflows/
```

### 3.2 Development Standards
- Establish coding standards and style guides
- Configure linting and formatting tools
- Set up pre-commit hooks
- Define git workflow and branching strategy
- **With Claude Code:** Generate project scaffolding, create CI/CD pipelines

## Phase 4: Incremental Development

### 4.1 Development Approach
Break solution into logical, testable modules:
1. **Data Ingestion Layer:** Source connectivity and raw data landing
2. **Transformation Layer:** Business logic and data enrichment
3. **Quality Layer:** Validation and monitoring
4. **Serving Layer:** Final tables and API endpoints

### 4.2 Agentic Development Workflow

#### Task Definition
Create detailed task files in `agent-prompts/tasks/` for each module:
```markdown
# agent-prompts/tasks/ingestion/s3_ingestion.md
## TASK: S3 to Iceberg Ingestion Pipeline

## OBJECTIVE
Build production-ready ingestion pipeline from S3 to Iceberg

## FILES TO CREATE
- src/ingestion/s3_to_iceberg.py
- airflow/dags/ingestion/s3_ingestion_dag.py
- tests/test_s3_ingestion.py

## SPECIFICATIONS
[Detailed requirements]
```

#### Prompt Execution with Claude
Use explicit context pattern (Option 2):
```bash
claude-code "Create S3 ingestion pipeline as defined in agent-prompts/tasks/ingestion/s3_ingestion.md. Use schemas/raw_events_schema.yaml and follow standards/error_handling.md"
```

#### Prompt Documentation
Save executed prompts for audit and reuse:
```markdown
# agent-prompts/executed_prompts/2025-01-15_s3_ingestion_v1.md
## Timestamp: 2025-01-15 10:30:00
## Developer: [Name]
## Claude Model: claude-3-opus

## PROMPT
Create S3 ingestion pipeline as defined in agent-prompts/tasks/ingestion/s3_ingestion.md. 
Use schemas/raw_events_schema.yaml and follow standards/error_handling.md

## CONTEXT FILES REFERENCED
- agent-prompts/tasks/ingestion/s3_ingestion.md
- agent-prompts/schemas/raw_events_schema.yaml
- agent-prompts/standards/error_handling.md

## OUTCOME
- Generated: src/ingestion/s3_to_iceberg.py (450 lines)
- Generated: airflow/dags/ingestion/s3_ingestion_dag.py (120 lines)
- Status: SUCCESS
- Notes: Added retry logic for transient S3 errors
```

### 4.3 Component Development Patterns

#### Spark Components (No Executors)
Direct Spark job pattern:
```python
# src/ingestion/s3_to_iceberg.py
def main():
    args = parse_arguments()
    spark = create_spark_session()
    
    try:
        # Business logic
        df = read_source_data(spark, args)
        validated_df = validate_schema(df, args.schema)
        enriched_df = add_metadata(validated_df)
        write_to_iceberg(enriched_df, args.target_table)
    finally:
        spark.stop()
```

#### Airflow DAGs (Orchestration Layer)
DAG-to-DAG orchestration:
```python
# airflow/dags/orchestration/daily_pipeline_dag.py
with DAG("daily_master_pipeline", ...) as dag:
    trigger_ingestion = TriggerDagRunOperator(
        task_id="trigger_ingestion",
        trigger_dag_id="s3_ingestion",
        conf={"date": "{{ ds }}"},
        wait_for_completion=True
    )
```

#### Data Quality with Great Expectations
Integrated validation:
```python
# src/validation/great_expectations_runner.py
def run_validation(spark_df, expectations_suite):
    ge_df = ge.dataset.SparkDFDataset(spark_df)
    results = ge_df.validate(expectations_suite)
    if not results.success:
        raise DataQualityException(results)
    return results
```

## Phase 5: Integration & Testing

### 5.1 Integration Testing
- End-to-end pipeline execution
- Cross-system data validation
- Performance benchmarking
- Failure recovery testing
- **With Claude:** Generate test scenarios and validation scripts

### 5.2 Data Quality Implementation
- Deploy Great Expectations checkpoints
- Configure quality thresholds
- Set up alerting and notifications
- Create quality dashboards
- **With Claude:** Generate quality monitoring queries

### 5.3 Performance Optimization
- Analyze Spark execution plans
- Optimize join strategies and shuffles
- Tune Iceberg table properties
- Configure resource allocation
- **With Claude:** Analyze performance metrics and suggest optimizations

## Phase 6: Deployment & Operations

### 6.1 Deployment Preparation
- Environment configuration management
- Secret and credential management
- Infrastructure as Code setup
- Rollback procedure documentation
- **With Claude Code:** Generate deployment automation scripts

### 6.2 Monitoring & Observability
- Airflow task monitoring and alerting
- Spark job performance dashboards
- Data quality trend analysis
- Metabase dashboard creation
- **With Claude:** Generate monitoring queries and alert configurations

### 6.3 Production Readiness
- Disaster recovery procedures
- Data retention and archival policies
- Cost monitoring and optimization
- SLA tracking and reporting
- **With Claude:** Create operational runbooks

## Phase 7: Maintenance & Evolution

### 7.1 Continuous Improvement
- Performance trend analysis
- Cost optimization reviews
- Quality metric evaluation
- User feedback incorporation
- **With Claude:** Analyze metrics and suggest improvements

### 7.2 Knowledge Management
- Document lessons learned
- Update best practices library
- Maintain solution catalog
- Train team members
- **With Claude:** Generate knowledge base articles

## Best Practices for Claude Integration

### Agentic Development Workflow

#### 1. Task Definition Structure
```markdown
# agent-prompts/tasks/[module]/[feature].md
## TASK: [Clear, actionable title]

## OBJECTIVE
[1-2 sentences describing the goal]

## FILES TO CREATE
- [List all files to be generated]

## SPECIFICATIONS
- [ ] Requirement 1
- [ ] Requirement 2

## DEPENDENCIES
- Schema: schemas/[schema_file].yaml
- Standards: standards/[standard].md
- Template: examples/[template].py
```

#### 2. Prompt Execution Pattern
Always use explicit context (Option 2):
```bash
claude-code "Create [feature] as defined in agent-prompts/tasks/[module]/[feature].md. Use schemas/[schema].yaml and follow standards/[standard].md"
```

#### 3. Prompt Documentation
```markdown
# agent-prompts/executed_prompts/YYYY-MM-DD_feature_version.md
## Metadata
- Timestamp: YYYY-MM-DD HH:MM:SS
- Developer: [Name]
- Claude Model: [Model]
- Task Reference: tasks/[module]/[feature].md

## PROMPT
[Exact prompt used]

## CONTEXT FILES
- [List all referenced files]

## OUTCOME
- Generated: [file] ([lines] lines)
- Modified: [file] ([changes])
- Status: SUCCESS/PARTIAL/FAILED
- Notes: [Any important observations]

## FOLLOW-UP PROMPTS
[Any refinement prompts used]
```

#### 4. Context File Organization

##### Project Context (context.yaml)
```yaml
project: Data Platform
version: 1.0.0
updated: YYYY-MM-DD

tech_stack:
  orchestration:
    tool: Apache Airflow
    version: 2.8.0
  processing:
    tool: Apache Spark
    version: 3.5.0
  storage:
    tool: Apache Iceberg
    version: 1.4.0

constraints:
  spark:
    max_executors: 20
    executor_memory: 16GB
  airflow:
    max_parallel_tasks: 50
  
patterns:
  dag_structure: "orchestration-focused"
  error_handling: "fail-fast"
  logging: "structured-json"
```

##### Standards Documentation
```markdown
# agent-prompts/standards/error_handling.md
## Error Handling Standards

### Spark Jobs
- Wrap main logic in try-finally
- Log errors with correlation_id
- Clean up resources in finally

### Example
```python
correlation_id = str(uuid.uuid4())
logger.info(f"Starting job", extra={"correlation_id": correlation_id})
try:
    # Main logic
except Exception as e:
    logger.error(f"Job failed: {str(e)}", extra={"correlation_id": correlation_id})
    raise
finally:
    spark.stop()
```
```

### Quality Assurance with Claude

#### Code Review Prompt
```bash
claude "Review src/ingestion/s3_to_iceberg.py against standards/code_quality.md. Check for error handling, logging, and performance issues."
```

#### Test Generation
```bash
claude-code "Generate comprehensive tests for src/ingestion/s3_to_iceberg.py. Include unit tests for each function and integration tests with mock data."
```

#### Documentation Generation
```bash
claude "Generate technical documentation for the S3 ingestion module. Include architecture decisions, data flow, and troubleshooting guide."
```

### Iterative Refinement Process

1. **Initial Implementation**
   ```bash
   claude-code "Implement agent-prompts/tasks/ingestion/s3_basic.md"
   ```

2. **Add Error Handling**
   ```bash
   claude-code "Enhance s3_to_iceberg.py with comprehensive error handling from standards/error_handling.md"
   ```

3. **Optimize Performance**
   ```bash
   claude-code "Optimize s3_to_iceberg.py for 10GB files. Add partition pruning and adaptive query execution."
   ```

4. **Add Monitoring**
   ```bash
   claude-code "Add CloudWatch metrics to s3_to_iceberg.py following standards/monitoring.md"
   ```

### Success Metrics for Agentic Development

1. **Code Generation Efficiency:** 80% less time for initial implementation
2. **Consistency:** 100% adherence to defined standards
3. **Test Coverage:** Automated generation of 90%+ test coverage
4. **Documentation:** Complete technical docs with every module
5. **Reusability:** Patterns captured and reused across modules

## DataOps Integration

### Alignment with DataOps Principles

This framework aligns with modern DataOps practices by:

1. **Treating Data as Code**: Version control for all data pipelines and transformations
2. **CI/CD for Data**: Automated testing and deployment of data pipelines
3. **Continuous Monitoring**: Real-time data quality and pipeline health tracking
4. **Collaboration**: Breaking down silos between data producers and consumers

### Data Versioning Strategy

Consider implementing data versioning tools to enable:
- **Branching**: Isolated development environments for data
- **Time Travel**: Ability to reproduce past states
- **Rollback**: Safe recovery from data quality issues

**Recommended Tools**:
- **lakeFS**: Git-like operations for data lakes
- **DVC (Data Version Control)**: Version control for ML datasets
- **Delta Lake**: ACID transactions with time travel

### Monitoring & Observability

Implement comprehensive data observability:

1. **Pipeline Monitoring**
   - Job execution status and duration
   - Resource utilization metrics
   - Data freshness indicators

2. **Data Quality Monitoring**
   - Automated anomaly detection
   - Schema change alerts
   - Data drift monitoring

3. **Lineage Tracking**
   - Automated data lineage capture
   - Impact analysis for changes
   - Dependency visualization

**Recommended Tools**:
- **Monte Carlo**: Data observability platform
- **Great Expectations**: Data validation and profiling
- **Apache Atlas**: Metadata management and lineage

## Success Metrics

1. **Development Velocity:** Time from requirement to production
2. **Code Quality:** Test coverage, linting scores, review feedback
3. **System Reliability:** Uptime, error rates, SLA compliance
4. **Data Quality:** Validation pass rates, quality scores
5. **Cost Efficiency:** Processing cost per record, resource utilization

## Document Deliverables by Phase

### Phase 1: Discovery & Requirements
- Business Requirements Document
- Technical Assessment Report
- Data Profiling Report
- Source System Inventory
- Stakeholder Matrix

### Phase 2: Architecture & Design
- Solution Architecture Document
- Data Flow Diagrams
- Data Model Specifications
- Security & Compliance Design
- Technology Decision Records

### Phase 3: Development Environment Setup
- Development Standards Guide
- Project Setup Instructions
- CI/CD Configuration
- Environment Configuration Guide
- Git Workflow Documentation
- Agent Prompts Structure (`agent-prompts/`)
  - `context.yaml` - Project configuration
  - `tasks/` - Module specifications
  - `schemas/` - Data schemas
  - `standards/` - Coding standards
  - `examples/` - Code templates
  - `executed_prompts/` - Prompt audit trail

### Phase 4: Incremental Development
- Module Specification Documents (`agent-prompts/tasks/`)
- API Documentation
- Code Review Checklists
- Unit Test Reports
- Performance Benchmarks
- Executed Prompts Log (`agent-prompts/executed_prompts/`)
- Claude Interaction Patterns

### Phase 5: Integration & Testing
- Integration Test Plans
- Test Execution Reports
- Data Quality Rules Catalog
- Performance Optimization Report
- Quality Dashboard Designs

### Phase 6: Deployment & Operations
- Deployment Guide
- Operational Runbooks
- Monitoring Configuration
- Disaster Recovery Plan
- SLA Tracking Reports

### Phase 7: Maintenance & Evolution
- Lessons Learned Document
- Best Practices Catalog
- Knowledge Base Articles
- Training Materials
- Continuous Improvement Reports
- Prompt Evolution History

## References and Additional Resources

### Primary References

1. **Data Engineering Best Practices** - RishabhSoft  
   https://www.rishabhsoft.com/blog/data-engineering-best-practices  
   Comprehensive guide covering DataOps, automation, and modern data engineering practices

2. **Data Engineering Best Practices to Follow in 2025** - lakeFS  
   https://lakefs.io/blog/data-engineering-best-practices/  
   Focus on data versioning, CI/CD for data, and reproducibility in data engineering

3. **DataOps Explained: How To Not Screw It Up** - Monte Carlo  
   https://www.montecarlodata.com/blog-what-is-dataops/  
   Deep dive into DataOps principles, observability, and implementation strategies

4. **Best Practices And Benefits Of DevOps For Data Engineering** - Sparity  
   https://www.sparity.com/blogs/devops-for-data-engineering-and-dataops/  
   Integration of DevOps practices with data engineering workflows

### Additional Resources

- **Apache Airflow Documentation**: https://airflow.apache.org/docs/
- **Apache Spark Best Practices**: https://spark.apache.org/docs/latest/
- **Great Expectations Documentation**: https://docs.greatexpectations.io/
- **Apache Iceberg Documentation**: https://iceberg.apache.org/docs/

### Community and Support

- **Data Engineering Community**: r/dataengineering
- **Apache Airflow Slack**: https://apache-airflow-slack.herokuapp.com/
- **dbt Community**: https://www.getdbt.com/community/

---

*Last Updated: January 2025*  
*Version: 1.0*