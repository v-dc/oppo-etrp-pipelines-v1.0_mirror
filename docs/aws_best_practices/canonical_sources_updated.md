# Canonical Reference Sources

1. **AWS Well-Architected Framework**
   * 📄 PDF: https://docs.aws.amazon.com/pdfs/wellarchitected/2022-03-31/framework/wellarchitected-framework-2022-03-31.pdf
   * 🌐 HTML: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html
   * **Purpose:** Establishes foundational design principles across six pillars: Security, Reliability, Performance Efficiency, Cost Optimization, Operational Excellence, and Sustainability.

2. **Apache Airflow on Amazon MWAA**
   * 🌐 https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html
   * **Purpose:** Operational and configuration limits for running DAGs with Airflow on AWS (Managed Workflows for Apache Airflow).

3. **Apache Iceberg on AWS (Glue + S3)**
   * 🌐 https://iceberg.apache.org/aws/
   * 🌐 https://docs.aws.amazon.com/glue/latest/dg/iceberg.html
   * **Purpose:** Table format guidance for schema evolution, Iceberg compaction, and large-scale data lakes on S3.

4. **AWS Glue Data Catalog & Job Automation**
   * 🌐 https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html
   * **Purpose:** Central service for schema discovery, ETL job execution, and metadata versioning.

5. **Apache Spark on AWS Deployment Options**
   * 🌐 EMR: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html
   * 🌐 Glue Spark: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html
   * 🌐 EKS Spark: https://docs.aws.amazon.com/eks/latest/userguide/spark.html
   * 🌐 Spark on Fargate: https://aws.amazon.com/blogs/containers/running-spark-jobs-on-aws-fargate/
   * **Purpose:** Compare managed vs container-based Spark execution for different data processing patterns and workload requirements.

6. **Amazon S3 Performance and Layout Best Practices**
   * 🌐 https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
   * **Purpose:** Design performant and cost-efficient S3 folder layouts for ingestion, Iceberg, and archival.

7. **PostgreSQL on AWS (Amazon RDS & Aurora)**
   * 🌐 RDS PostgreSQL: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html
   * 🌐 Aurora PostgreSQL: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.html
   * **Purpose:** Compare performance, cost, and high availability for structured query and metadata workloads.

8. **AWS Security Best Practices for Data Workloads**
   * 🌐 https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/
   * **Purpose:** Detailed IAM controls, encryption, least-privilege access, and threat mitigation practices for analytics and storage layers.

9. **Modern Data Lake Architectures on AWS**
   * 🌐 https://docs.aws.amazon.com/whitepapers/latest/build-modern-data-lake/index.html
   * **Purpose:** End-to-end data lake design covering ingestion, cataloging, transformation, and serving.

10. **Data Quality Automation with AWS Glue, Lambda, and CloudWatch**
    * 🌐 https://aws.amazon.com/blogs/big-data/building-data-quality-rules/
    * **Purpose:** Event-driven data quality rule orchestration, alerts, and DQ metric publishing pipelines.