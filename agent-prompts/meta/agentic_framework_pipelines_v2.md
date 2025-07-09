# Agentic Framework Pipelines v1.0

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

### 2.1 Solution Decomposition (Step 2A)
- Design optimal module structure for agentic code generation
- Define clear module boundaries and responsibilities
- Size modules appropriately for Claude Code generation (200-400 lines)
- Minimize dependencies between modules
- **With Claude:** Generate module decomposition optimized for independent development

### 2.2 Solution Architecture (Step 2B)
- Design end-to-end data flow architecture using module decomposition
- Define component interactions and boundaries
- Plan for scalability and fault tolerance
- Design metadata and catalog strategy
- **With Claude:** Generate architecture diagrams (Mermaid), review patterns, validate design

### 2.3 Data Modeling
- Design dimensional/analytical models
- Define Iceberg table schemas and partitioning
- Plan slowly changing dimension strategies
- Design data quality framework
- **With Claude:** Generate DDL, optimize schemas, create naming conventions

### 2.4 Security & Compliance Design
- Define access control requirements
- Plan data encryption and masking
- Design audit logging strategy
- Document compliance requirements (GDPR, HIPAA, etc.)
- **With Claude:** Generate security policies, create compliance checklists

## Phase 3: Development Environment Setup

### 3.1 Project Structure

```
project-root/
├── agent-prompts/                    # Agentic framework (separate IP)
│   ├── requirements/                 # [Phase 1] Requirements analysis
│   │   ├── business_requirements.md  # [Phase 1] Business objectives and success criteria
│   │   ├── technical_assessment.md   # [Phase 1] Infrastructure and technical evaluation
│   │   └── data_discovery.md         # [Phase 1] Data profiling and source analysis
│   ├── design/                       # System design documents
│   │   ├── architecture.md           # [Phase 2] System components and technology stack
│   │   ├── data_flows.md             # [Phase 2] Data processing flows and diagrams
│   │   ├── design_decisions.md       # [Phase 2] Architecture Decision Records
│   │   └── implementation_plan.md    # [Phase 2] Complete system modules and implementation steps
│   ├── context/                      # Project context
│   │   ├── system_context.yaml       # [Phase 3] Machine-readable config
│   │   ├── data_context.md           # [Phase 3] Data specifications
│   │   └── technology/               # [Phase 3,4] Technology guidance
│   ├── meta/                         # [Phase 0] Framework governance
│   │   ├── framework_evolution_guide.md # [Phase 0] How Claude Code evolves framework
│   │   ├── revised_prompt_strategy.md   # [Phase 0] Prompt engineering guidelines
│   │   ├── context_file_standards.md    # [Phase 0] Documentation format standards
│   │   ├── discovery_templates.md       # [Phase 0] Templates for documenting discoveries
│   │   ├── framework_changelog.md       # [Phase 0] Framework change tracking
│   │   ├── module_closure_prompts.md    # [Phase 0] Human prompts for module closure
│   │   └── project_structure_standard.md # [Phase 0] Project creation template
│   ├── tasks/                        # [Phase 4] Module task specifications
│   ├── progress/                     # [Phase 4] Development tracking
│   │   ├── current_module_status.md  # Real-time module progress
│   │   ├── project_status.md         # Overall project status and learnings
│   │   ├── decisions_log.md          # Architecture decisions with evolution
│   │   ├── next_module_guide.md      # Human workflow for next module
│   │   └── executed_prompts/         # Audit trail of AI interactions
│   ├── examples/                     # [Phase 3] Code templates
│   └── standards/                    # [Phase 3] Development procedures
│       ├── development_patterns.md   # CB-Core specific patterns and conventions
│       └── [other standards files]
├── setup-scripts/                   # [Phase 3] Environment setup automation
├── configs/                         # [Phase 3] Application configuration files
├── src/                             # [Phase 4] Main codebase
│   └── common/                      # Shared utilities
├── great-expectations/              # [Phase 4] Quality framework
├── tests/                          # [Phase 4] Test suite
├── scripts/                        # [Phase 4] Utility scripts
└── logs/                           # [Phase 4] Application logs
```

### 3.2 Development Standards
- Establish coding standards and style guides
- Configure linting and formatting tools
- Set up pre-commit hooks
- Define git workflow and branching strategy
- **With Claude Code:** Generate project scaffolding, create CI/CD pipelines

### 3.3 Files Required Before Phase 4 (Iterative Development)

#### Phase 1 Completion:
- `requirements/business_requirements.md` - Business objectives and success criteria
- `requirements/technical_assessment.md` - Infrastructure and technical evaluation  
- `requirements/data_discovery.md` - Data profiling and source analysis

#### Phase 2 Completion:
- `design/module_structure.yaml` - Module decomposition optimized for agentic development
- `design/architecture_rationale.md` - Justification for module design decisions
- `design/architecture.md` - Complete system design
- `design/data_flows.md` - All data processing flows documented  
- `design/design_decisions.md` - Key architectural decisions recorded
- `design/implementation_plan.md` - Complete module roadmap

#### Phase 3 Completion:
- `context/system_context.yaml` - Machine-readable project configuration
- `context/data_context.md` - Data specifications and processing requirements
- `meta/` - All framework governance documents (copied from Phase 0 template)
- `examples/` - Code templates for the technology stack
- `standards/` - Development procedures, quality guidelines, and core development patterns for Claude Code
- `setup-scripts/` - Environment automation ready
- `configs/` - Application configuration prepared

## Phase 4: Incremental Development

### 4.1 Development Approach
Break solution into logical, testable modules:
- **Data Ingestion Layer:** Source connectivity and raw data landing
- **Transformation Layer:** Business logic and data enrichment
- **Quality Layer:** Validation and monitoring
- **Serving Layer:** Final tables and API endpoints

### 4.2 Agentic Development Workflow

#### Task Definition Structure

```markdown
# agent-prompts/tasks/[module]/[feature].md
## TASK: [Clear, actionable title]
## DELIVERABLES: [Concrete outputs with exact filenames]
- [List all files to be generated]
## SUCCESS CRITERIA: [Measurable outcomes with checkboxes]
- [ ] Requirement 1
- [ ] Requirement 2
## CONTEXT FILES: [Dependencies before implementation]
- Schema: context/data_context.md
- Standards: standards/development_patterns.md
- Template: examples/[template].py
## TECHNICAL SPECIFICATIONS: [Implementation details]
[Detailed requirements including data flow, infrastructure, and quality requirements]
## CONSTRAINTS & STANDARDS: [Boundaries and quality requirements]
[Security, compatibility, and scalability considerations]
```

#### Prompt Execution Pattern by Project Type

**Implementation/Development Tasks** (building something new):
```bash
claude-code "TASK: Create [feature] as defined in agent-prompts/tasks/[module]/[feature].md. 
DELIVERABLES: [specific files]
SUCCESS CRITERIA: [validation requirements]
CONTEXT FILES: Use context/system_context.yaml and follow standards/development_patterns.md
TECHNICAL SPECIFICATIONS: [how to build it]
CONSTRAINTS: [quality boundaries]"
```

**Integration/Migration Tasks** (working within existing systems):
```bash
claude-code "TASK: [integration task]
CONTEXT FILES: Review design/architecture.md and context/data_context.md first
TECHNICAL SPECIFICATIONS: [how to work within constraints]
SUCCESS CRITERIA: [validation of integration]
DELIVERABLES: [outputs]
CONSTRAINTS: [boundaries]"
```

#### Prompt Documentation and Progress Tracking
Save executed prompts in `progress/executed_prompts/` for audit and reuse:

```markdown
# agent-prompts/progress/executed_prompts/2025-01-15_s3_ingestion_v1.md
## Metadata
- Timestamp: 2025-01-15 10:30:00
- Developer: [Name]
- Claude Model: claude-sonnet-4
- Task Reference: tasks/ingestion/s3_ingestion.md
## PROMPT
Create S3 ingestion pipeline as defined in agent-prompts/tasks/ingestion/s3_ingestion.md. 
Use context/system_context.yaml and follow standards/development_patterns.md
## CONTEXT FILES REFERENCED
- agent-prompts/tasks/ingestion/s3_ingestion.md
- agent-prompts/context/system_context.yaml
- agent-prompts/standards/development_patterns.md
## OUTCOME
- Generated: src/ingestion/s3_to_iceberg.py (450 lines)
- Generated: tests/test_s3_ingestion.py (120 lines)
- Status: SUCCESS
- Notes: Added retry logic for transient S3 errors
## FOLLOW-UP PROMPTS
[Any refinement prompts used]
```

#### Module Progress Tracking
Maintain real-time status in `progress/current_module_status.md`:

```markdown
# Current Module Status
## Module: S3 Ingestion Pipeline
## Status: IN_PROGRESS
## Completion: 75%
## Next Steps:
- [ ] Add error handling for network timeouts
- [ ] Create integration tests
- [ ] Update documentation
## Blockers: None
## Notes: Performance optimization needed for large files
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

**Project Context (context/system_context.yaml)**

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

**Data Context (context/data_context.md)**

```markdown
# Data Context
## Data Sources
- S3 buckets: raw-events, processed-data
- Database: PostgreSQL production, Iceberg analytics
## Processing Requirements
- Real-time: < 5 minute latency
- Batch: Daily aggregations
- Quality: 99.9% accuracy threshold
## Schema Standards
- All timestamps in UTC
- Required fields: event_id, timestamp, source_system
- Data retention: 7 years
```

**Standards Documentation (standards/development_patterns.md)**

```markdown
---
title: Development Patterns
purpose: CB-Core specific patterns and conventions for Claude Code
audience: [claude-code]
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 1.0
related_files: [context/system_context.yaml, examples/spark_job_template.py]
---

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

## Validation
- [ ] All functions have correlation_id logging
- [ ] Resource cleanup in finally blocks
- [ ] Structured JSON logging format
```

### Quality Assurance with Claude

#### Code Review Prompt
```bash
claude "Review src/ingestion/s3_to_iceberg.py against standards/development_patterns.md. Check for error handling, logging, and performance issues."
```

#### Test Generation
```bash
claude-code "Generate comprehensive tests for src/ingestion/s3_to_iceberg.py. Include unit tests for each function and integration tests with mock data."
```

#### Documentation Generation
```bash
claude "Generate technical documentation for the S3 ingestion module. Include architecture decisions, data flow, and troubleshooting guide."
```

### Project Initialization Checklist

#### Phase 1 Complete:
- [ ] `requirements/business_requirements.md` - Business objectives and success criteria
- [ ] `requirements/technical_assessment.md` - Infrastructure and technical evaluation
- [ ] `requirements/data_discovery.md` - Data profiling and source analysis

#### Phase 2 Complete:
- [ ] `design/module_structure.yaml` - Module decomposition optimized for agentic development
- [ ] `design/architecture_rationale.md` - Justification for module design decisions
- [ ] `design/architecture.md` - Complete system design
- [ ] `design/data_flows.md` - All data processing flows documented  
- [ ] `design/design_decisions.md` - Key architectural decisions recorded
- [ ] `design/implementation_plan.md` - Complete module roadmap

#### Phase 3 Complete:
- [ ] Project folder structure created
- [ ] `context/system_context.yaml` - Project-specific configuration
- [ ] `context/data_context.md` - Data specifications
- [ ] `meta/` - Framework governance documents copied
- [ ] `examples/` - Identify and add applicable code templates for the technology stack
- [ ] `standards/` - Development procedures, quality guidelines, and core development patterns for Claude Code
- [ ] `setup-scripts/` - Environment automation ready
- [ ] `configs/` - Application configuration prepared

#### Ready for Phase 4:
- [ ] All required files in place
- [ ] Framework governance available
- [ ] First module task specification ready
- [ ] Development environment prepared

### Iterative Refinement Process

#### Initial Implementation
```bash
claude-code "Implement agent-prompts/tasks/ingestion/s3_basic.md"
```

#### Add Error Handling
```bash
claude-code "Enhance s3_to_iceberg.py with comprehensive error handling from standards/error_handling.md"
```

#### Optimize Performance
```bash
claude-code "Optimize s3_to_iceberg.py for 10GB files. Add partition pruning and adaptive query execution."
```

#### Add Monitoring
```bash
claude-code "Add CloudWatch metrics to s3_to_iceberg.py following standards/monitoring.md"
```

### Success Metrics for Agentic Development
- **Code Generation Efficiency:** 80% less time for initial implementation
- **Consistency:** 100% adherence to defined standards
- **Test Coverage:** Automated generation of 90%+ test coverage
- **Documentation:** Complete technical docs with every module
- **Reusability:** Patterns captured and reused across modules

## DataOps Integration

### Alignment with DataOps Principles
This framework aligns with modern DataOps practices by:
- **Treating Data as Code:** Version control for all data pipelines and transformations
- **CI/CD for Data:** Automated testing and deployment of data pipelines
- **Continuous Monitoring:** Real-time data quality and pipeline health tracking
- **Collaboration:** Breaking down silos between data producers and consumers

### Data Versioning Strategy
Consider implementing data versioning tools to enable:
- **Branching:** Isolated development environments for data
- **Time Travel:** Ability to reproduce past states
- **Rollback:** Safe recovery from data quality issues

**Recommended Tools:**
- **lakeFS:** Git-like operations for data lakes
- **DVC (Data Version Control):** Version control for ML datasets
- **Delta Lake:** ACID transactions with time travel

### Monitoring & Observability
Implement comprehensive data observability:

#### Pipeline Monitoring
- Job execution status and duration
- Resource utilization metrics
- Data freshness indicators

#### Data Quality Monitoring
- Automated anomaly detection
- Schema change alerts
- Data drift monitoring

#### Lineage Tracking
- Automated data lineage capture
- Impact analysis for changes
- Dependency visualization

**Recommended Tools:**
- **Monte Carlo:** Data observability platform
- **Great Expectations:** Data validation and profiling
- **Apache Atlas:** Metadata management and lineage

### Success Metrics
- **Development Velocity:** Time from requirement to production
- **Code Quality:** Test coverage, linting scores, review feedback
- **System Reliability:** Uptime, error rates, SLA compliance
- **Data Quality:** Validation pass rates, quality scores
- **Cost Efficiency:** Processing cost per record, resource utilization

## Document Deliverables by Phase

### Phase 1: Discovery & Requirements
- Business Requirements Document
- Technical Assessment Report
- Data Profiling Report
- Source System Inventory
- Stakeholder Matrix

### Phase 2: Architecture & Design
- Solution Architecture Document
- Module Decomposition (module_structure.yaml)
- Architecture Rationale (architecture_rationale.md)
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
- **Agent Prompts Structure (agent-prompts/)**
  - context.yaml - Project configuration
  - tasks/ - Module specifications
  - schemas/ - Data schemas
  - standards/ - Coding standards
  - examples/ - Code templates
  - executed_prompts/ - Prompt audit trail

### Phase 4: Incremental Development
- Module Specification Documents (agent-prompts/tasks/)
- API Documentation
- Code Review Checklists
- Unit Test Reports
- Performance Benchmarks
- **Progress Tracking (agent-prompts/progress/)**
  - current_module_status.md - Real-time module progress
  - project_status.md - Overall project status and learnings
  - decisions_log.md - Architecture decisions with evolution
  - next_module_guide.md - Human workflow for next module
  - executed_prompts/ - Audit trail of AI interactions
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
- **Framework Evolution History (agent-prompts/meta/)**
  - framework_changelog.md - Framework change tracking
  - framework_evolution_guide.md - How Claude Code evolves framework

## References and Additional Resources

### Primary References
- **Data Engineering Best Practices - RishabhSoft**  
  [Top 12 Data Engineering Best Practices for Your Business](https://www.rishabhsoft.com/blog/data-engineering-best-practices)  
  Comprehensive guide covering DataOps, automation, and modern data engineering practices

- **Data Engineering Best Practices to Follow in 2025 - lakeFS**  
  [15 Data Engineering Best Practices to Follow in 2025](https://lakefs.io/blog/data-engineering-best-practices/)  
  Focus on data versioning, CI/CD for data, and reproducibility in data engineering

- **DataOps Explained: How To Not Screw It Up - Monte Carlo**  
  [DataOps Explained: How To Not Screw It Up](https://www.montecarlodata.com/blog-dataops-explained/)  
  Deep dive into DataOps principles, observability, and implementation strategies

- **Best Practices And Benefits Of DevOps For Data Engineering - Sparity**  
  [Best Practices and Benefits of DevOps for Data Engineering and DataOps in 2024](https://sparity.co/blog/devops-for-data-engineering-best-practices/)  
  Integration of DevOps practices with data engineering workflows

### Additional Resources
- **Apache Airflow Documentation:** [Documentation](https://airflow.apache.org/docs/)
- **Apache Spark Best Practices:** [Overview - Spark 3.5.x Documentation](https://spark.apache.org/docs/3.5.0/)
- **Great Expectations Documentation:** [Home | Great Expectations](https://greatexpectations.io/)
- **Apache Iceberg Documentation:** [Overview](https://iceberg.apache.org/)

### Community and Support
- **Data Engineering Community:** [r/dataengineering](https://www.reddit.com/r/dataengineering/)
- **Apache Airflow Slack:** [Join the Apache Airflow Community community on Slack!](https://apache-airflow-slack.herokuapp.com/)
- **dbt Community:** [Join the dbt Community — collaborate & grow in data | dbt Labs](https://www.getdbt.com/community/)

---

**Last Updated:** January 2025  
**Version:** 1.0