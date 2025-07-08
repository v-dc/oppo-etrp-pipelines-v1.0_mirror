# AWS Services Available in Malaysia (ap-southeast-5)

## Reference Sources
- **Official:** [AWS Regional Services](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) (Select Asia Pacific Malaysia)
- **Unofficial (Verified):** [AWS Services Info - Malaysia](https://www.aws-services.info/ap-southeast-5.html)

## Purpose
This file provides a reference for checking AWS service availability in the Asia Pacific (Malaysia) region (ap-southeast-5) for eTR+ pipeline design decisions.

**Latest Update:** July 2025 (Based on official AWS sources)

---

## Source Credibility Assessment

**Unofficial Source Verification:** The aws-services.info website appears to be **credible and accurate** based on cross-reference with official AWS data:
- Service names match official AWS terminology exactly
- Date tracking appears consistent with AWS service launch patterns
- The site explicitly states it's a "daily feed from AWS public information"
- Service availability aligns with official AWS regional services page
- Includes proper disclaimers about being unofficial

**Recommendation:** Use official AWS source as primary reference, but unofficial source can serve as a quick lookup tool for service availability checks.

---

## AWS Services Currently Available in Malaysia (ap-southeast-5)

### Core Compute & Infrastructure
- Amazon Elastic Compute Cloud (EC2)
- Amazon Elastic Block Store (EBS)
- Amazon EC2 Auto Scaling
- AWS Fargate
- Amazon Elastic Container Service (ECS)
- Amazon Elastic Kubernetes Service (EKS)
- Amazon Elastic Container Registry (ECR)
- Amazon Elastic File System (EFS)
- AWS Batch

### Storage & Content Delivery
- Amazon Simple Storage Service (S3)
- Amazon CloudFront
- AWS DataSync
- AWS Storage Gateway
- Amazon FSx (Lustre, NetApp ONTAP, OpenZFS, Windows File Server)

### Database Services
- Amazon Relational Database Service (RDS)
- Amazon Aurora
- Amazon DynamoDB
- Amazon DynamoDB Streams
- Amazon ElastiCache
- Amazon Redshift
- Amazon Neptune

### Analytics & Big Data
- **AWS Glue** ✅ (Available since Nov 2024)
- **Amazon Athena** ✅ (Available since Dec 2024)
- **AWS Lake Formation** ✅ (Available since Nov 2024)
- **Amazon EMR** ✅ (Available)
- **Amazon Managed Workflows for Apache Airflow (MWAA)** ✅ (Available since Jun 2025)
- Amazon Kinesis Data Streams
- Amazon Data Firehose
- Amazon OpenSearch Service
- Amazon Managed Streaming for Apache Kafka (MSK)
- Amazon Managed Service for Apache Flink

### Networking & Security
- Amazon Virtual Private Cloud (VPC)
- AWS Direct Connect
- AWS PrivateLink
- AWS Transit Gateway
- AWS VPN
- AWS Key Management Service (KMS)
- AWS Secrets Manager
- AWS Certificate Manager
- AWS Private Certificate Authority
- AWS Identity and Access Management (IAM)
- AWS IAM Identity Center
- Amazon GuardDuty
- AWS Security Hub
- AWS Config
- AWS CloudTrail
- AWS WAF
- AWS Shield
- AWS Network Firewall

### Management & Governance
- AWS CloudFormation
- Amazon CloudWatch
- Amazon CloudWatch Logs
- AWS Systems Manager
- AWS Organizations
- AWS Control Tower
- AWS Backup
- AWS Health Dashboard
- AWS X-Ray
- AWS Trusted Advisor

### Developer Tools & Integration
- AWS Lambda
- Amazon API Gateway
- Amazon EventBridge
- Amazon Simple Notification Service (SNS)
- Amazon Simple Queue Service (SQS)
- AWS Step Functions
- AWS CodePipeline
- Amazon Cognito

### Application Services
- Amazon Route 53
- AWS App Config
- AWS AppSync
- Amazon MQ
- Amazon Polly

### Machine Learning
- Amazon SageMaker
- Amazon SageMaker AI

### Monitoring & Observability
- Amazon Managed Service for Prometheus

---

## Key Observations for eTR+ Pipeline Design

### ✅ **Pipeline-Critical Services Available:**
- **MWAA** (Airflow orchestration) - Available since June 2025
- **AWS Glue** (ETL processing) - Available since November 2024
- **Lake Formation** (Data governance) - Available since November 2024
- **Athena** (Query engine) - Available since December 2024
- **EMR** (Spark processing) - Available
- **S3** (Data lake storage) - Available
- **RDS/Aurora** (PostgreSQL for operations DB) - Available

### 📋 **Design Implications:**
- **All core services for the eTR+ BNPL pipeline are available in Malaysia**
- Recent additions (MWAA, Glue, Lake Formation, Athena) indicate AWS is actively expanding analytics capabilities in the region
- No major service gaps that would require cross-region dependencies
- Can implement the full modern data lake architecture within ap-southeast-5

### ⚠️ **Considerations:**
- Some services are relatively new to the region - monitor for stability and feature parity
- Cross-reference specific features within services (e.g., Glue catalog integration with Iceberg)
- Consider data residency requirements for financial services compliance

---

## Quick Service Lookup Pattern
Use this pattern to verify service availability:
1. Check official AWS Regional Services page first
2. Cross-reference with aws-services.info for quick validation
3. Note launch dates for newer services to assess maturity
4. Verify specific feature availability within services

> **Note:** Service availability can change rapidly. Always verify current status during implementation planning.