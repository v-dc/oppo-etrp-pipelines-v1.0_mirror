# Self-Managed Airflow Deployment Options on AWS

## Reference
- [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Airflow on Kubernetes](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [EKS Best Practices for Airflow](https://aws.github.io/aws-eks-best-practices/cost-optimization/workloads/)

## Purpose
This file provides deployment patterns for self-managed Apache Airflow on AWS as alternatives to Amazon MWAA. Covers architecture options, operational considerations, and cost comparisons for informed orchestration decisions.

**Latest Update:** July 2025

---

## Self-Managed Airflow vs MWAA

### **Key Differences:**
- **Cost**: Potentially 30-70% lower for medium-large workloads
- **Versions**: Access to latest Airflow releases (2.10+, Python 3.12)
- **Customization**: No plugin size limits or packaging restrictions
- **Control**: Full configuration and scaling control
- **Overhead**: Higher operational complexity and maintenance burden

---

## Deployment Options Comparison

| Option | Complexity | Cost (Medium Scale) | Scalability | Maintenance | Best For |
|--------|------------|---------------------|-------------|-------------|----------|
| **EKS + Helm** | High | $200-400/month | Excellent | High | Production, multi-tenant |
| **ECS + Fargate** | Medium | $150-300/month | Good | Medium | Simpler deployments |
| **EC2 + Docker** | Medium | $100-250/month | Limited | Medium | Small teams, cost-sensitive |
| **EKS + Operators** | Very High | $250-500/month | Excellent | Very High | Advanced K8s teams |
| **Serverless Components** | Low | $50-150/month | Limited | Low | Development, testing |

**MWAA Comparison**: $300-600/month for small environment

### **Complexity Levels:**

**High:** Kubernetes knowledge, Helm configuration, multi-service networking, persistent volumes, complex debugging across K8s and Airflow layers.

**Medium:** Container concepts, AWS service fundamentals, standard debugging. Fewer moving parts than Kubernetes.

**Very High:** All Kubernetes complexity plus dynamic pod lifecycle management, advanced resource optimization, performance tuning.

**Low:** AWS Lambda, Step Functions, EventBridge basics. Event-driven patterns with AWS-managed infrastructure.

### **Cost Drivers:**

**EKS + Helm:** EKS control plane ($75) + worker nodes ($100-250) + RDS ($50-100) + storage/LB ($20-40)
**ECS + Fargate:** Scheduler task ($30-50) + worker tasks ($80-200) + RDS/storage ($50-70)
**EC2 + Docker:** EC2 instances ($70-180) + RDS ($50-100) + EBS storage ($10-30)
**Serverless:** Lambda executions ($10-80) + Step Functions ($20-50) + storage ($5-20)

### **Scalability Patterns:**

**Excellent:** Horizontal Pod Autoscaler, Cluster Autoscaler, custom resource requirements per task, multi-AZ deployment
**Good:** Service Auto Scaling, independent service scaling, limited by Fargate maximums (30GB memory)
**Limited:** Manual capacity planning, single-instance bounds, Lambda timeout limits (15 min)

### **Maintenance Overhead:**

**High/Very High:** Cluster upgrades, security patches, complex monitoring, multi-layer troubleshooting, K8s expertise required
**Medium:** Container updates, standard AWS maintenance, simpler monitoring scope
**Low:** AWS-managed infrastructure, simple deployments, automatic security updates

---

## Decision Framework

### **Workload Assessment Questions:**

**Scale:**
- How many DAGs will you manage? (< 10 / 10-50 / 50+)
- What's your expected daily task volume? (< 100 / 100-1000 / 1000+)
- How many concurrent tasks do you need? (< 10 / 10-100 / 100+)

**Workload Patterns:**
- Are workloads primarily batch or real-time?
- What are typical task durations? (< 5min / 5-30min / > 30min)
- Do tasks have variable resource requirements?

**Team Capabilities:**
- What's your team's Kubernetes experience level? (None / Basic / Expert)
- What operational overhead can you accept? (Low / Medium / High)
- Do you need multiple environments? (Dev only / Dev+Prod / Full SDLC)

**Requirements:**
- What are your cost constraints? (Very tight / Moderate / Flexible)
- Are there data sovereignty requirements?
- What SLA/uptime requirements do you have? (Dev/Test / Production / Mission-critical)

### **Service Availability (Malaysia ap-southeast-5):**
- **EKS**: ✅ Available
- **ECS/Fargate**: ✅ Available  
- **EC2**: ✅ Available
- **Lambda/Step Functions**: ✅ Available
- **RDS PostgreSQL**: ✅ Available
- **EFS/EBS**: ✅ Available

---

## 1. Amazon EKS with Helm Chart (Recommended)

### **Architecture Overview**
- **Orchestration**: EKS cluster with Airflow Helm chart
- **Components**: Webserver, Scheduler, Workers (CeleryExecutor)
- **Storage**: EFS for DAGs, RDS PostgreSQL for metadata
- **Scaling**: Horizontal Pod Autoscaler + Cluster Autoscaler

### **Deployment Pattern**
```yaml
# values.yaml for Airflow Helm chart
airflow:
  version: "2.10.1"
  executor: "CeleryExecutor"
  
workers:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 10

postgresql:
  enabled: false  # Use external RDS
  
redis:
  enabled: true  # For Celery message broker

dags:
  persistence:
    enabled: true
    storageClassName: "efs-sc"
```

### **Cost Breakdown (Medium Scale)**
- **EKS Cluster**: $75/month (control plane)
- **Worker Nodes**: $150-300/month (3x m5.large with spot)
- **RDS PostgreSQL**: $50-100/month (db.t3.medium)
- **EFS Storage**: $10-20/month
- **Load Balancer**: $20/month
- **Total**: ~$305-515/month

### **Pros:**
- Latest Airflow versions and features
- Excellent horizontal scaling
- Cloud-native architecture
- Full Kubernetes ecosystem benefits

### **Cons:**
- High operational complexity
- Requires Kubernetes expertise
- More moving parts to manage

---

## 2. Amazon ECS with Fargate

### **Architecture Overview**
- **Orchestration**: ECS cluster with Fargate tasks
- **Components**: Separate services for webserver, scheduler, workers
- **Storage**: EFS for DAGs, RDS for metadata
- **Scaling**: ECS Service Auto Scaling

### **Task Definitions**
```json
{
  "family": "airflow-scheduler",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [{
    "name": "airflow-scheduler",
    "image": "apache/airflow:2.10.1",
    "command": ["scheduler"],
    "mountPoints": [{
      "sourceVolume": "dags",
      "containerPath": "/opt/airflow/dags"
    }]
  }]
}
```

### **Cost Breakdown (Medium Scale)**
- **Fargate Tasks**: $120-250/month (scheduler + 2-4 workers)
- **RDS PostgreSQL**: $50-100/month
- **EFS Storage**: $10-20/month
- **Application Load Balancer**: $20/month
- **ElastiCache Redis**: $30-50/month
- **Total**: ~$230-440/month

### **Pros:**
- Serverless container execution
- Simpler than Kubernetes
- Good auto-scaling capabilities
- AWS-native service integration

### **Cons:**
- Limited to Fargate constraints (30GB memory)
- Less flexible than EKS
- Fargate pricing can be higher than EC2

---

## 3. EC2 with Docker Compose

### **Architecture Overview**
- **Deployment**: Single or multi-instance setup with Docker Compose
- **Components**: All services on same instances
- **Storage**: EBS volumes for DAGs, external RDS
- **Scaling**: Manual or Auto Scaling Groups

### **Docker Compose Example**
```yaml
version: '3.8'
services:
  airflow-webserver:
    image: apache/airflow:2.10.1
    command: webserver
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    
  airflow-scheduler:
    image: apache/airflow:2.10.1
    command: scheduler
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
```

### **Cost Breakdown (Small-Medium Scale)**
- **EC2 Instances**: $70-200/month (2x m5.large with spot)
- **RDS PostgreSQL**: $50-100/month
- **EBS Storage**: $20-40/month
- **Load Balancer**: $20/month (optional)
- **Total**: ~$160-360/month

### **Pros:**
- Simplest setup and management
- Lowest cost for small workloads
- Direct instance access for debugging
- Full control over environment

### **Cons:**
- Limited horizontal scaling
- Manual operational overhead
- Single points of failure
- Less cloud-native

---

## 4. EKS with Kubernetes-Native Operators

### **Architecture Overview**
- **Orchestration**: EKS with Airflow Kubernetes Executor
- **Execution**: Each task runs as separate Kubernetes pod
- **Scaling**: True elastic scaling per task
- **Isolation**: Complete task isolation and resource control

### **Configuration**
```python
# airflow.cfg
[kubernetes]
namespace = airflow
worker_container_repository = apache/airflow
worker_container_tag = 2.10.1
delete_worker_pods = True
worker_pods_creation_batch_size = 16

[core]
executor = KubernetesExecutor
```

### **Cost Breakdown (Variable Load)**
- **EKS Cluster**: $75/month
- **Node Pool**: $100-400/month (spot instances, auto-scaling)
- **RDS PostgreSQL**: $50-100/month
- **EFS Storage**: $10-20/month
- **Total**: ~$235-595/month (highly variable)

### **Pros:**
- Maximum scalability and efficiency
- Perfect resource isolation
- Cloud-native task execution
- Cost-efficient for variable workloads

### **Cons:**
- Most complex setup
- Requires advanced Kubernetes knowledge
- Potential pod startup overhead
- Network and storage considerations

---

## 5. Serverless Components Pattern

### **Architecture Overview**
- **Scheduler**: Lambda function triggered by CloudWatch Events
- **Execution**: Step Functions or Lambda for simple workflows
- **Storage**: S3 for DAGs/code, DynamoDB for state
- **UI**: Optional - static site or simple API

### **Use Cases**
- Development and testing environments
- Simple, low-frequency workflows
- Event-driven data processing
- Cost-sensitive scenarios

### **Cost Breakdown (Light Usage)**
- **Lambda Executions**: $10-50/month
- **Step Functions**: $20-80/month
- **DynamoDB**: $5-25/month
- **S3 Storage**: $5-15/month
- **Total**: ~$40-170/month

### **Pros:**
- Lowest cost for light usage
- Zero operational overhead
- Pay-per-execution model
- Serverless benefits

### **Cons:**
- Limited Airflow compatibility
- No web UI (unless custom)
- Simple workflows only
- AWS service limits

---

## Integration with eTR+ Pipeline

### **Common Integration Patterns:**
```python
# Glue Job Execution
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

glue_task = GlueJobOperator(
    task_id='process_bnpl_data',
    job_name='bnpl-etl-job',
    script_location='s3://dags/scripts/transform.py'
)

# EMR Cluster Operations  
from airflow.providers.amazon.aws.operators.emr import EMRCreateJobFlowOperator

emr_task = EMRCreateJobFlowOperator(
    task_id='large_batch_processing',
    job_flow_overrides=emr_config
)

# ECS Task Execution
from airflow.providers.amazon.aws.operators.ecs import ECSOperator

ecs_task = ECSOperator(
    task_id='data_quality_check',
    cluster='airflow-cluster',
    task_definition='dq-check-task'
)
```

### **Key Operational Considerations:**
- **Security**: IAM roles, VPC configuration, secrets management
- **Monitoring**: CloudWatch integration, custom metrics, alerting
- **Backup**: Metadata database, DAG versioning, configuration management
- **CI/CD**: Automated DAG deployment, environment promotion

---

