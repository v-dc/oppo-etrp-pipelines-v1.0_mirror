# Airflow on Amazon MWAA: Architecture & Design Context

## Reference
- [Amazon MWAA User Guide](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
- [MWAA CI/CD Best Practices](https://aws.amazon.com/blogs/opensource/deploying-to-amazon-managed-workflows-for-apache-airflow-with-ci-cd-tools/)

## Purpose
This file captures technical constraints, capabilities, and best practices for using Apache Airflow via Amazon Managed Workflows for Apache Airflow (MWAA) as the orchestration layer in a modern AWS-based data pipeline.

---

## Overview
Amazon MWAA is a fully managed service that makes it easy to run Apache Airflow at scale on AWS.

### Key Capabilities
- Native support for Airflow 2.x versions
- Automatic scaling of workers
- Built-in logging with CloudWatch
- Secure access to Amazon S3, AWS Secrets Manager, Amazon RDS, etc.
- DAGs stored in S3
- Role-based execution with managed IAM policies

---

## Version Support
- **Current Latest:** Airflow 2.10.1 + Python 3.10.8
- **Airflow 3.0:** Not supported (self-managed required)
- **Python 3.12:** Not supported (use containerized tasks for newer Python)
- **Deprecation:** v2.4.3, v2.5.1, v2.6.3 end support December 30, 2025

---

## Core Architecture
- **DAG Location:** DAGs are stored in a versioned S3 bucket
- **Orchestration:** Scheduler polls DAGs and tasks are executed by MWAA workers on Fargate containers
- **Metadata DB:** PostgreSQL hosted and managed by AWS
- **Logs:** CloudWatch (separate log streams for tasks, workers, scheduler)
- **Authentication:** IAM-based + optionally integrated with AWS SSO

---

## Key Limits & Environment Classes

| Resource                 | Limit                     |
|--------------------------|---------------------------|
| Max DAGs                | 1000                      |
| Max concurrent tasks    | Based on environment class|
| Max workers             | 25 (environment dependent)|
| Max plugins             | 100MB (via zip upload)   |
| DAG sync time           | ~30s (updates), ~300s (new)|
| Environment classes     | small/medium/large/xlarge |
| Scheduler heartbeat     | ~10s                      |
| DAG parse timeout       | ~30s                      |

---

## Network Requirements
- **VPC:** 2+ private subnets, NAT Gateway for external access
- **Access Modes:** Public (internet) or Private (VPC-only)
- **Security:** IAM-based authentication, KMS encryption default
- **S3 Bucket:** Must start with `airflow-` prefix, versioning enabled

---

## CI/CD Best Practice
- **DAGs:** Deploy immediately to S3 (no restart required)
- **Plugins/Requirements:** Require environment update (downtime)
- **Recommended:** Separate DAG and plugin deployment lifecycles
- **Structure:** Use CodePipeline or GitHub Actions to sync DAGs to S3
- **Secrets:** Store credentials in Secrets Manager and access via Airflow connections

---

## Cost Considerations
- Charged based on MWAA environment uptime + worker duration
- Additional charges: CloudWatch Logs, S3 access, Secrets Manager, RDS PostgreSQL
- Scale environment size (small, medium, large) to match expected concurrency

---

## When *Not* to Use MWAA
- You require Airflow 3.0 or Python 3.12
- You require exotic plugins with C extensions
- Your DAGs require more than 100 concurrent tasks *sustained*
- You want Kubernetes-native orchestration (use self-hosted Airflow on EKS instead)

---

## Integration with Spark, Iceberg, and Glue
- Airflow DAGs can trigger:
  - AWS Glue jobs via `GlueJobOperator`
  - Spark jobs on EMR via `EMROperator`
  - EKS Spark jobs via `EKSPodOperator`
  - Iceberg compaction and metadata ops via containerized tasks

---

## Summary
MWAA is suitable as the orchestration layer for the eTR+ platform, assuming DAGs are well-structured, task concurrency is managed, and plugins are limited in size.

> Recommended for: **Pipeline coordination**, **Monitoring**, **Triggering Glue/Spark Jobs**, **Parallel control of ingest + validation workflows**