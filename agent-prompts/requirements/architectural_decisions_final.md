# CTOS eTR+ Architectural Decisions Document

## Executive Summary
Critical technology decisions for the CTOS eTR+ platform rebuild, ranked by impact on 5x volume growth, CCA 2025 compliance timeline, cost optimization, and operational complexity.

---

## Decision Ranking

**1. [Data Processing Engine](#1-data-processing-engine-decision) - HIGHEST IMPACT**  
**2. [Orchestration Platform](#2-orchestration-platform-decision) - HIGH IMPACT**  
**3. [Operational Database](#3-operational-database-decision) - HIGH IMPACT**  
**4. [Attribute Engine](#4-attribute-engine-decision) - HIGH IMPACT**  
**5. [Data Lake Architecture](#5-data-lake-architecture-decision) - MEDIUM IMPACT**  
**6. [Quality & Monitoring](#6-quality--monitoring-decision) - MEDIUM IMPACT**  
**7. [Security Architecture](#7-security-architecture-decision) - MEDIUM IMPACT**

---

## 1. Data Processing Engine Decision

**Requirements:** 700K→3.5M monthly records, distributed processing, memory optimization, Great Expectations integration

### Options Evaluated
- **AWS Glue**: Serverless Spark, auto-scaling, $0.44/DPU-hour
- **EMR Clusters**: Full Spark control, estimated cluster sizing below
- **EMR Serverless**: Pay-per-job (NOT available in Malaysia)

**EMR Cluster Sizing for 3.5M Monthly Records:**
- **Master**: 1 x m5.xlarge (4 vCPU, 16GB)
- **Core**: 3 x m5.xlarge (12 vCPU, 48GB total)  
- **Task**: 2 x m5.xlarge (8 vCPU, 16GB, spot instances)
- **Processing Window**: 8 hours/day batch processing
- **Estimated Cost**: $800-1,000/month (with spot instances + optimized scheduling)

### **Recommendation: AWS Glue**

**Rationale:**
- **Serverless scaling** handles 5x volume growth automatically
- **Malaysia region** fully available with Glue 5.0 (Spark 3.5.4)
- **Cost efficiency** for variable BNPL workloads vs fixed EMR clusters
- **Great Expectations** native integration available
- **Iceberg support** built-in for data lake architecture

**Key Trade-offs:**
- ✅ **Benefits**: No cluster management, auto-scaling, AWS service integration
- ❌ **Limitations**: Less customization than EMR, cold start latency (1-2 min)
- 💰 **Cost**: ~$1,200/month estimated for 5x volume vs $800-1,000/month for optimized EMR clusters

**Implementation Impact:** 
- Timeline: Faster development (no cluster setup/management)
- Skills: Lower learning curve than EMR cluster optimization
- Operations: Zero infrastructure management vs cluster monitoring/tuning

---

## 2. Orchestration Platform Decision

**Requirements:** Workflow management, 5x growth support, exception handling, Malaysia region compliance

### Options Evaluated
- **Amazon MWAA**: Managed Airflow, $300-400/month small environment
- **Self-managed Airflow on EKS**: $200-400/month, Kubernetes-based orchestration
- **Self-managed Airflow on ECS**: $230-440/month, container-based orchestration

**EKS Airflow Setup (High Control):**
- **EKS Cluster**: $72/month (24/7) + worker nodes
- **Worker Nodes**: 3 x t3.medium ($50/month with spot instances)
- **RDS PostgreSQL**: $50/month (metadata database)
- **Load Balancer**: $20/month
- **Total**: ~$200-300/month
- **Complexity**: High (Kubernetes management, Helm charts, pod scheduling)

**ECS Airflow Setup (Medium Control):**
- **ECS Fargate Tasks**: Scheduler + webserver + 2-4 workers ($120-250/month)
- **RDS PostgreSQL**: $50-100/month
- **Application Load Balancer**: $20/month
- **EFS Storage**: $10-20/month (DAGs storage)
- **Total**: ~$230-440/month  
- **Complexity**: Medium (container orchestration, less complex than Kubernetes)

**Key Differences:**
- **MWAA**: Fully managed, zero infrastructure, built-in scaling, AWS service integration
- **EKS**: Maximum control, latest Airflow versions, Kubernetes ecosystem, requires K8s expertise
- **ECS**: Simpler than EKS, container-native, AWS Fargate serverless execution, moderate complexity

### **Recommendation: Self-managed Airflow on ECS**

**Rationale:**
- **Cost efficient** at $230-440/month vs $300-400/month for MWAA
- **AWS-native containers** with Fargate serverless execution reduces operational complexity
- **Moderate learning curve** - container concepts simpler than Kubernetes
- **Full control** over Airflow versions and plugins without MWAA limitations
- **Team growth** - builds valuable containerization skills for modern data architecture

**Key Trade-offs:**
- ✅ **Benefits**: Cost savings, full Airflow control, serverless worker scaling, good AWS integration, skill building
- ❌ **Limitations**: 1-2 weeks setup time, requires container knowledge, moderate operational overhead
- 💰 **Cost**: $230-440/month vs $300-400/month (MWAA) vs $200-300/month (EKS)

**Self-Managed Trade-offs:**
- **EKS Pros**: Latest Airflow versions, unlimited customization, Kubernetes ecosystem integration
- **EKS Cons**: Requires Kubernetes expertise, complex setup (2-3 weeks), ongoing cluster management
- **ECS Pros**: Simpler than EKS, AWS Fargate serverless workers, good AWS integration  
- **ECS Cons**: Less flexible than EKS, still requires container orchestration knowledge

**Implementation Impact:**
- **ECS**: 1-2 weeks setup, moderate container knowledge required, balanced complexity vs control
- **MWAA Alternative**: Immediate start but higher ongoing costs and plugin limitations
- **EKS Alternative**: 2-3 weeks setup, requires Kubernetes training, high operational complexity

---

## 3. Operational Database Decision

**Requirements:** PostgreSQL, real-time queries, attribute engine support, high availability

### Options Evaluated
- **RDS PostgreSQL**: $91/month (r6g.large), traditional setup
- **Aurora PostgreSQL**: $182/month (r6g.large), cloud-native
- **Aurora Serverless v2**: $65+/month, auto-scaling

### **Recommendation: Aurora PostgreSQL**

**Rationale:**
- **99.99% SLA** critical for operational queries and attribute engine
- **3x performance** improvement over standard PostgreSQL
- **Auto-scaling storage** 10GB-128TB handles growth seamlessly
- **Sub-10ms replica lag** for read scaling of attribute calculations

**Key Trade-offs:**
- ✅ **Benefits**: Superior performance, automatic failover (30s), 6-way replication
- ❌ **Limitations**: 2x cost of RDS PostgreSQL, Aurora-specific features
- 💰 **Cost**: $182/month vs $91/month RDS PostgreSQL

**Implementation Impact:**
- Performance: Better support for on-demand attribute calculations
- Reliability: Higher availability for business-critical operations

---

## 4. Attribute Engine Decision

**Requirements:** Calculate characteristics on top of raw data, on-demand for live reports, batch for retrospective enquiries

### Options Evaluated
- **SageMaker Feature Store**: Managed AWS feature engineering platform, $0.0035/1,000 operations
- **Custom PostgreSQL Solution**: In-database stored procedures and views for calculations
- **DeepCredit Solution**: Purpose-built credit bureau attribute engine (custom development)

**DeepCredit Solution Specifications:**
- **Development Stack**: Python/FastAPI, Redis caching, PostgreSQL, Docker containers
- **Architecture**: Microservices with calculation engine, cache layer, API gateway
- **Features**: Credit-specific algorithms, regulatory calculations, real-time scoring
- **Development Time**: 6-9 months full-stack development
- **Team Requirements**: 3-4 developers (backend, frontend, DevOps, credit domain expert)
- **Estimated Cost**: $300K-500K development + $50-100/month operational costs

### **Recommendation: SageMaker Feature Store**

**Rationale:**
- **Credit-Agnostic Flexibility**: Can implement any credit-specific calculation while leveraging managed infrastructure
- **Faster Time-to-Market**: 2-3 months vs 6-9 months for custom DeepCredit solution
- **Risk Mitigation**: Proven AWS service vs untested custom development
- **Dual Storage Strategy**: Built-in online/offline stores perfect for live vs batch requirements
- **Integration Benefits**: Native AWS ecosystem integration with Glue, Athena, Lambda

**Key Trade-offs:**
- ✅ **Benefits**: Managed scaling, built-in audit trails, proven reliability, faster delivery
- ❌ **Limitations**: Higher operational cost vs custom solution, learning curve for credit-specific implementation
- 💰 **Cost**: ~$200-400/month operational vs $50-100/month custom solution + $300K-500K development

**DeepCredit Alternative Analysis:**
- **Custom Advantages**: Perfect credit bureau fit, lower operational costs, full control
- **Custom Disadvantages**: High development risk, 6-9 month timeline conflicts with CCA 2025, ongoing maintenance burden
- **Technical Complexity**: Requires building caching, scaling, monitoring, security from scratch

**Implementation Impact:**
- Timeline: Accelerates delivery by 4-6 months vs DeepCredit development
- Risk: Lower risk with managed service vs custom development unknowns
- Expertise: Leverages AWS skills vs requiring specialized fintech development team

---

## 5. Data Lake Architecture Decision

**Requirements:** Iceberg warehouse, ACID transactions, schema evolution, 7-year retention

### Options Evaluated
- **S3 + Iceberg + Glue Catalog**: Native AWS integration
- **S3 + Delta Lake + Custom Catalog**: Alternative table format
- **Traditional Parquet + Partitioning**: Simpler but less capable

### **Recommendation: S3 + Iceberg + Glue Catalog**

**Rationale:**
- **Native Glue support** with Iceberg 1.7.1 in Malaysia region
- **ACID transactions** required for data consistency with corrections/patches
- **Schema evolution** critical for 35+ contributor layout variations
- **Time travel** capabilities for audit trails and historical analysis

**Key Trade-offs:**
- ✅ **Benefits**: ACID compliance, schema flexibility, cross-service compatibility
- ❌ **Limitations**: Learning curve, more complex than Parquet
- 💰 **Cost**: Standard S3 pricing + metadata overhead (~5% additional)

**Implementation Impact:**
- Capability: Enables attribute engine complex calculations
- Maintenance: Built-in compaction and optimization

---

## 6. Quality & Monitoring Decision

**Requirements:** Great Expectations integration, real-time monitoring, operational dashboards

### Options Evaluated
- **Great Expectations on Glue + CloudWatch**: AWS-native monitoring
- **Custom validation + CloudWatch Dashboards**: Build vs buy
- **Third-party monitoring tools**: External solutions

### **Recommendation: Great Expectations on Glue + CloudWatch**

**Rationale:**
- **Existing framework** in current pipeline reduces migration risk
- **Glue integration** available for distributed validation
- **CloudWatch native** dashboards for operational visibility
- **Airflow integration** for automated quality workflows

**Key Trade-offs:**
- ✅ **Benefits**: Proven framework, AWS integration, existing team knowledge
- ❌ **Limitations**: Limited real-time capabilities, CloudWatch costs
- 💰 **Cost**: CloudWatch costs ~$80/month + GE execution costs

**Implementation Impact:**
- Migration: Easier transition from existing Great Expectations setup
- Operations: Familiar tools for data engineering team

---

## 7. Security Architecture Decision

**Requirements:** Malaysia data residency, CCA 2025 compliance, encryption, audit trails

### Options Evaluated
- **AWS KMS + IAM + VPC**: Standard AWS security stack
- **Customer-managed encryption**: Higher control, more complexity
- **AWS native services only**: Simplicity vs feature gaps

### **Recommendation: AWS KMS + IAM + VPC**

**Rationale:**
- **Malaysia region compliance** all security services available
- **KMS encryption** at rest/transit with automatic key rotation
- **IAM least privilege** with service-specific roles
- **VPC isolation** for network security

**Key Trade-offs:**
- ✅ **Benefits**: Managed security services, compliance-ready, audit integration
- ❌ **Limitations**: AWS vendor lock-in for security services
- 💰 **Cost**: KMS ~$20/month + VPC costs

**Implementation Impact:**
- Compliance: Meets CCA 2025 audit requirements
- Operations: Automated security management

---

## Cost Summary

| Component | Monthly Cost | Annual Cost | 5-Year Total |
|-----------|-------------|-------------|--------------|
| **AWS Glue** (5x volume) | $1,200 | $14,400 | $72,000 |
| **ECS Airflow** | $320 | $3,840 | $19,200 |
| **Aurora PostgreSQL** | $200 | $2,400 | $12,000 |
| **S3 + Lifecycle** | $150 | $1,800 | $9,000 |
| **SageMaker Feature Store** | $300 | $3,600 | $18,000 |
| **CloudWatch + KMS** | $100 | $1,200 | $6,000 |
| **Total Estimated** | **$2,270** | **$27,240** | **$136,200** |

*Note: Costs scale with actual usage; estimates based on 5x volume projection. DeepCredit alternative would require additional $300K-500K upfront development cost.*

---

## Implementation Timeline Impact

### Critical Path Dependencies
1. **ECS Environment Setup** (Week 1): Required for Airflow deployment and configuration
2. **SageMaker Feature Store Setup** (Week 2): Required for attribute engine capabilities
3. **Glue Jobs Development** (Weeks 2-4): Core processing pipeline
4. **Aurora Setup** (Week 2): Parallel with Glue development
5. **Iceberg Integration** (Weeks 3-5): After basic Glue pipeline working

### Risk Mitigation
- **ECS learning curve**: Allocate 1-2 weeks for team container training and setup
- **Glue learning curve**: Allocate extra time for team Spark optimization training
- **Aurora migration**: Plan parallel running with existing PostgreSQL

---

## Decision Validation Criteria

### Must Achieve by December 2025
- [ ] Process 3.5M monthly records within SLA
- [ ] Zero data loss during production migration  
- [ ] Meet CCA 2025 audit and compliance requirements
- [ ] Reduce manual intervention by significant margin

### Success Metrics
- **Volume Handling**: 5x capacity confirmed through load testing
- **Cost Efficiency**: Total cost within projected $2,270/month (excluding DeepCredit development costs)
- **Operational Excellence**: <5% manual intervention rate
- **Regulatory Compliance**: Pass audit requirements
- **Attribute Engine**: Sub-second response for real-time calculations, efficient batch processing

---

**Document Owner**: CTOS Technical Architecture Team  
**Decision Date**: July 2025  
**Review Frequency**: Monthly during implementation  
**Final Approval Required**: Technical Lead and Business Stakeholders