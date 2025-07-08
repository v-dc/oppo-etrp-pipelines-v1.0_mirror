# ✅ Updated Context `.md` Files for AWS-Based eTR+ Design

1. **`aws_well_architected_summary.md`**  
   **Purpose:** Core principles to reference for any design decision  
   **Contents:**
   * Summary of the 6 AWS Well-Architected pillars
   * Key trade-off principles (e.g., scalability vs. cost, automation vs. complexity)
   * Relevant best practices for data pipelines and analytics workloads

2. **`spark_on_aws_deployment_options.md`**  
   **Purpose:** Compare Spark deployment patterns on AWS for data pipeline workloads  
   **Contents:**
   * EMR vs Glue vs EKS vs ECS vs EC2 for Spark execution
   * Performance characteristics (startup time, scaling, cost per job)
   * Integration patterns with orchestration systems
   * Malaysia regional availability updates
   * Cost optimization strategies (spot instances, auto-scaling, right-sizing)

3. **`airflow_mwaa_architecture.md`**  
   **Purpose:** Facts, limits, and options for Airflow on AWS  
   **Contents:**
   * MWAA vs self-managed comparison
   * Plugin support, environment variables, secrets
   * DAG deployment method, logs, alerting
   * Limits on DAG count, parallelism, environment configs
   * Example: CI/CD-friendly deployment structure

4. **`airflow_self_managed_options.md`**  
   **Purpose:** Self-managed Airflow deployment alternatives to MWAA  
   **Contents:**
   * EKS + Helm, ECS + Fargate, EC2 + Docker deployment options
   * Cost comparison and complexity analysis
   * Decision framework questions for option selection
   * Integration patterns with AWS services
   * Operational considerations and trade-offs

5. **`iceberg_on_s3_glue.md`**  
   **Purpose:** How Apache Iceberg works on AWS with Glue, Spark, and S3  
   **Contents:**
   * Iceberg table format advantages (schema evolution, partitioning, deletes)
   * S3 layout structure and Glue Catalog integration
   * Compatibility with Athena, Redshift Spectrum
   * Pitfalls (eventual consistency, commit race conditions)

6. **`aws_glue_catalog_and_jobs.md`**  
   **Purpose:** Catalog and job design for schema and batch automation  
   **Contents:**
   * Catalog structure: databases, tables, versions
   * Glue Jobs vs Glue Studio integration patterns
   * Trigger mechanisms (event, cron, pipeline-driven)
   * IAM roles, connection definitions

7. **`s3_best_practices_data_lake.md`**  
   **Purpose:** Layout guidance for scalable, Iceberg-compatible S3 design  
   **Contents:**
   * Folder structure for raw, staging, cleaned, enriched layers
   * Partitioning strategies
   * Request cost and performance tuning (prefixes, small files, compression)
   * Security and access control (bucket policies, encryption)

8. **`postgres_on_aws_options.md`**  
   **Purpose:** When to use RDS vs Aurora for transactional components  
   **Contents:**
   * Feature comparison
   * Performance/cost tradeoffs
   * Connection pooling
   * Backup and HA configurations

9. **`data_quality_automation_aws.md`**  
   **Purpose:** Patterns for automated DQ checks, alerts, and dashboards  
   **Contents:**
   * Framework to trigger validations using Airflow/Step Functions
   * Use of AWS Glue, Lambda, CloudWatch for monitoring
   * Storing metrics in RDS or Iceberg
   * Integration ideas with Great Expectations or custom code

10. **`aws_data_pipeline_reference_arch.md`**  
    **Purpose:** Template reference for modern data lake pipeline on AWS  
    **Contents:**
    * Standard components and flow: Ingestion → Lake → Transform → Serve
    * Integration patterns between all components
    * Where Spark fits, where Glue fits, where orchestration manages

11. **`aws_security_and_data_governance.md`**  
    **Purpose:** Baseline security and privacy policies for financial/regulated data  
    **Contents:**
    * IAM patterns: least privilege, role chaining
    * Encryption at rest and in transit (KMS, TLS)
    * Audit, logging, and data access tracking
    * Glue + Lake Formation governance options

12. **`aws_cost_control_for_etl.md`**  
    **Purpose:** Cost optimization strategies for data pipeline workloads  
    **Contents:**
    * Autoscaling vs reserved capacity for EMR/Spark
    * Orchestration environment tuning for cost
    * Glue cost per DPU-hour estimates
    * Cost implications of small files and S3 API usage
    * Spot instance strategies for Spark workloads
    * Right-sizing recommendations by workload type

13. **`aws_malaysia_services.md`**  
    **Purpose:** Service availability verification for Malaysia region  
    **Contents:**
    * Official vs unofficial source credibility assessment
    * Complete list of AWS services available in ap-southeast-5
    * Pipeline-critical services confirmation
    * Data sovereignty compliance implications