# Spark on AWS Deployment Options - Context

## Reference
- [EMR Spark Documentation](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [AWS Glue Spark Documentation](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html)
- [EKS Spark Documentation](https://docs.aws.amazon.com/eks/latest/userguide/spark.html)

## Purpose
Compare Spark deployment patterns on AWS for data pipeline workloads. Covers performance characteristics, cost models, and integration patterns with orchestration for informed architectural decisions.

---

## Deployment Options Comparison

| Option | Startup Time | Cost Model | Best Use Case |
|--------|--------------|------------|---------------|
| **EMR Clusters** | 5-15 min | Per-instance + EMR fee | Long-running, predictable workloads |
| **EMR Serverless** | 1-3 min | Pay per job (DPU-based) | Intermittent, variable workloads |
| **Glue (Serverless)** | 1-2 min | $0.44/DPU-hour | ETL jobs, schema evolution |
| **EMR on EKS** | 2-5 min | Per-instance + container overhead | Multi-tenant, K8s-native environments |
| **ECS/Fargate** | 1-2 min | Per-task pricing | Small jobs, event-driven processing |
| **EC2 Self-Managed** | Variable | Instance costs only | Full control, custom requirements |

---

## 1. Amazon EMR (Elastic MapReduce)

### **EMR Clusters (Most Mature)**
- **Performance**: Best for large-scale, long-running jobs
- **Cost**: $0.27/hr + EC2 instance costs (example: m5.xlarge ~$0.192/hr)
- **Scaling**: Manual or auto-scaling groups
- **Integration**: EMROperator, EMRJobFlowOperator in Airflow
- **Spot Support**: Up to 90% savings with mixed instance groups

### **EMR Serverless (Newer Option)**
- **Performance**: Up to 61% lower costs and 68% performance improvement vs open-source Spark on EKS
- **Cost**: Pay per job, automatic resource allocation
- **Scaling**: Automatic based on job requirements
- **Integration**: EMRServerlessOperator in Airflow
- **Best For**: Intermittent workloads, unpredictable schedules

---

## 2. AWS Glue (Serverless Spark)

### **Current Versions & Features**
- **Latest**: Glue 5.0 (Spark 3.5.4, Python 3.11, Java 17)
- **Iceberg Support**: Native support for Apache Iceberg, Hudi, Delta Lake
- **Auto-Scaling**: Available on Glue 3.0+ for dynamic resource allocation

### **Cost Structure**
- **Standard Jobs**: $0.44/DPU-hour, 1-minute minimum billing
- **Flex Execution**: ~25% cost savings for non-SLA workloads
- **Streaming**: G.025X worker type for low-volume streams (1/4 cost)

### **Limitations**
- **Memory**: Maximum 32GB executor memory (G2.X instances)
- **Customization**: Less flexible than EMR for complex configurations
- **Integration**: GlueJobOperator in Airflow

---

## 3. EMR on EKS (Container-Native)

### **Performance Advantages**
- **EMR Runtime**: 2.1x better geometric mean, 3.5x faster total runtime vs open-source Spark
- **Cost Optimization**: Graviton instances (15% performance, 30% cost savings)
- **Spot Integration**: Graceful executor decommissioning for Spot interruptions

### **Use Cases**
- Multi-tenant Spark environments
- Kubernetes-native data platforms
- Mixed workload environments (Spark + other K8s workloads)

### **Integration**
- **Airflow**: EKSPodOperator, custom Spark job submission
- **Operators**: Spark Operator or native spark-submit with EMR runtime

---

## 4. ECS/Fargate (Emerging Pattern)

### **Characteristics**
- **Serverless**: No cluster management overhead
- **Cost**: Pay per task duration
- **Memory Limits**: Up to 30GB per task (Fargate)
- **Best For**: Small to medium jobs, event-driven processing

### **Integration**
- **Airflow**: ECSOperator for containerized Spark jobs
- **Use Cases**: Data quality checks, small ETL transformations

---

## 5. Self-Managed on EC2

### **When to Consider**
- Need Airflow 3.0 or Python 3.12 (not available in managed services)
- Custom Spark builds or exotic dependencies
- Extreme cost optimization requirements
- Regulatory compliance requiring full control

### **Trade-offs**
- **Cost**: Lowest compute costs, highest operational overhead
- **Complexity**: Infrastructure management, security patching
- **Integration**: Custom operators or SSH/API-based task execution

---

## Performance & Cost Guidelines

### **Job Duration Considerations**
- **< 5 minutes**: Glue or ECS/Fargate
- **5-30 minutes**: Glue, EMR Serverless
- **30+ minutes**: EMR Clusters, EMR on EKS
- **Always-on**: EMR Clusters with auto-scaling

### **Data Volume Guidelines**
- **< 10GB**: Glue, ECS/Fargate
- **10GB-1TB**: Any option, choose based on frequency
- **> 1TB**: EMR Clusters or EMR on EKS for best performance

### **Cost Optimization Strategies**
- **Spot Instances**: EMR, EMR on EKS (up to 90% savings)
- **Reserved Capacity**: EMR Clusters for predictable workloads
- **Auto-Scaling**: Glue, EMR Serverless for variable workloads
- **Right-Sizing**: Monitor DPU/instance utilization

---

## Integration with Data Pipeline Stack

### **Iceberg Integration**
- **Glue**: Native Iceberg 1.7.1 support in Glue 5.0
- **EMR**: Full Iceberg feature support, custom versions
- **EKS**: Configurable Iceberg versions via custom images

### **Airflow Orchestration Patterns**
```python
# EMR Cluster
EMRJobFlowOperator(task_id="process_data", job_flow_overrides=config)

# Glue Job  
GlueJobOperator(task_id="etl_job", job_name="data_transform")

# EMR on EKS
EKSPodOperator(task_id="spark_job", image="emr-spark-image")
```

### **Data Catalog Integration**
- **Glue**: Native integration with Glue Data Catalog
- **EMR**: External metastore or Glue Catalog integration
- **All Options**: Support for schema evolution and partition management

---

## Decision Matrix

### **Choose EMR Clusters When:**
- Long-running, batch-oriented workloads
- Need full Hadoop ecosystem (Hive, HBase, Presto)
- Predictable resource requirements
- Complex multi-step processing pipelines

### **Choose Glue When:**
- Serverless ETL preferred
- Native AWS integration required
- Schema discovery and cataloging needed
- Variable or unpredictable workloads

### **Choose EMR on EKS When:**
- Multi-tenant environments
- Kubernetes-native architecture
- Mixed workload types (Spark + ML/AI)
- Need container orchestration benefits

### **Choose ECS/Fargate When:**
- Small, event-driven jobs
- Minimal infrastructure management
- Integration with existing ECS workflows

---

## Regional Availability in Malaysia (ap-southeast-5) - Updated July 2025

| Service/Option | Available in Malaysia | Available in Singapore | Information Freshness | Source |
|----------------|----------------------|------------------------|----------------------|---------|
| **EMR Clusters** | ✅ **Available** | ✅ Yes | July 2025 | [Malaysia Services Available](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) |
| **EMR Serverless** | ❌ **NOT Available** | ✅ Yes | July 2025 | AWS Regional Services |
| **AWS Glue** | ✅ **Available** | ✅ Yes | July 2025 | [Confirmed Available](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) |
| **Amazon EKS** | ✅ **Available** | ✅ Yes | July 2025 | Malaysia Launch Services |
| **ECS/Fargate** | ✅ **Available** | ✅ Yes | July 2025 | Malaysia Launch Documentation |
| **MWAA (for orchestration)** | ✅ **Available** | ✅ Yes | July 2025 | [MWAA Malaysia Launch June 2025](https://aws.amazon.com/about-aws/whats-new/2025/06/amazon-mwaa-additional-region/) |
| **Athena** | ✅ **Available** | ✅ Yes | July 2025 | Malaysia Regional Services |
| **Lake Formation** | ✅ **Available** | ✅ Yes | July 2025 | Malaysia Regional Services |
| **EC2 (Self-Managed)** | ✅ **Available** | ✅ Yes | July 2025 | Malaysia Launch Day 1 |

**✅ EXCELLENT NEWS FOR DATA SOVEREIGNTY:**

### **Malaysia Region (ap-southeast-5) Current Status:**
- **Launch Date**: August 22, 2024 (rapid service expansion)
- **Service Growth**: Significant expansion since launch
- **Analytics Stack**: Full modern data lake stack now available
- **Key Services Available**: EMR, Glue, MWAA, Athena, Lake Formation, S3, RDS

### **Recommended Spark Architecture for Malaysia:**
1. **AWS Glue (Serverless Spark)** ✅ **RECOMMENDED**
   - Native Iceberg support with Glue 5.0
   - Serverless auto-scaling
   - Integrated with Glue Data Catalog
   - Cost-effective for variable workloads

2. **EMR Clusters** ✅ Available
   - Best performance for large-scale processing
   - Full Hadoop ecosystem support
   - Spot instance support for cost optimization
   - Advanced Spark configurations

3. **EKS with Self-Managed Spark** ✅ Available
   - Maximum flexibility and control
   - Latest Spark versions (3.5+)
   - Container-native architecture
   - Good for multi-tenant environments

4. **ECS/Fargate Spark Jobs** ✅ Available
   - Event-driven processing
   - Smaller workloads
   - Quick startup times

### **Orchestration Options in Malaysia:**
- **Amazon MWAA** ✅ **Available** (since June 2025)
- **Self-Managed Airflow on EKS** ✅ Available (Alternative if MWAA not preferred)
- **AWS Step Functions** ✅ Available
- **EventBridge + Lambda** ✅ Available

### **Complete Analytics Stack Available:**
- **Data Lake**: S3 + Iceberg format support
- **ETL Processing**: Glue + EMR for Spark jobs
- **Orchestration**: MWAA or self-managed Airflow
- **Query Engine**: Athena for ad-hoc queries
- **Data Governance**: Lake Formation for permissions
- **Operations DB**: RDS/Aurora PostgreSQL

---

## Recommendations for eTR+ (Updated for Malaysia Region)

### **Primary Architecture (All Available in Malaysia):**
- **Primary Spark**: **AWS Glue** for serverless ETL jobs (native Iceberg support)
- **Secondary Spark**: **EMR Clusters** for large-scale processing with spot instances
- **Orchestration**: **MWAA** for managed Airflow (available since June 2025)
- **Alternative Orchestration**: **Self-managed Airflow on EKS** (if MWAA not preferred)
- **Data Lake**: **S3 + Iceberg** with **Lake Formation** governance
- **Query Engine**: **Athena** for ad-hoc analytics

### **Cost-Optimized Approach:**
- Use **Glue** for most ETL workloads (serverless, auto-scaling)
- Use **EMR with Spot instances** for large batch processing (up to 90% savings)
- **MWAA small environment** for orchestration (~$300-400/month base cost)
- **S3 Intelligent Tiering** for cost-optimized storage

### **If Not Using MWAA (Alternative Orchestration):**
- **Self-managed Airflow on EKS** with:
  - Latest Airflow 2.10+ versions
  - Custom operators and plugins
  - Full control over scaling and configuration
  - Integration with EKS cluster autoscaler
- **Cost**: Potentially lower than MWAA for large workloads
- **Effort**: Higher operational overhead

### **Key Considerations:**
- **EMR Serverless**: Not yet available in Malaysia - use EMR Clusters instead
- **Data Sovereignty**: All core services now available in ap-southeast-5
- **Cost**: Monitor Glue DPU usage and EMR instance utilization
- **Performance**: EMR provides better performance for large datasets (>1TB)
- **Flexibility**: Self-managed options provide latest versions and custom configurations