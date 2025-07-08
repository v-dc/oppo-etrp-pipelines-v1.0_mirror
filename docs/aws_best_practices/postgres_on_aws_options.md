# PostgreSQL on AWS Deployment Options

## Reference
- [Amazon RDS PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [Amazon Aurora PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.html)
- [RDS vs Aurora Comparison](https://aws.amazon.com/rds/aurora/postgresql-features/)

## Purpose
This file compares PostgreSQL deployment options on AWS for transactional workloads, focusing on the operations database component of the eTR+ pipeline. Covers feature comparison, performance characteristics, and cost considerations.

**Latest Update:** July 2025

---

## Deployment Options Comparison

| Option | Use Case | Availability | Backup/Recovery | Cost Model | Best For |
|--------|----------|--------------|-----------------|------------|----------|
| **RDS PostgreSQL** | Traditional OLTP | Single-AZ, Multi-AZ | Automated, Point-in-time | Standard pricing | Predictable workloads |
| **Aurora PostgreSQL** | Cloud-native OLTP | Multi-AZ by design | Continuous backup | Pay-per-I/O available | Variable workloads |
| **Aurora Serverless v2** | Auto-scaling OLTP | Multi-AZ serverless | Continuous backup | Pay-per-ACU | Intermittent workloads |
| **RDS Proxy** | Connection pooling | Works with RDS/Aurora | Transparent | Additional cost | High-connection apps |

---

## 1. Amazon RDS PostgreSQL

### **Architecture**
- **Traditional Database**: Single primary instance with optional read replicas
- **Storage**: EBS-based with gp3, io1, or io2 options
- **Scaling**: Vertical scaling (instance size) and horizontal (read replicas)
- **Availability**: Single-AZ or Multi-AZ deployment

### **Key Features**
- **PostgreSQL Versions**: 12.x through 16.x supported
- **Extensions**: 85+ supported extensions including PostGIS, pg_stat_statements
- **Performance Insights**: Built-in performance monitoring
- **Blue/Green Deployments**: Zero-downtime version upgrades

### **Storage Options**
- **General Purpose (gp3)**: 3,000 IOPS baseline, burstable to 16,000
- **Provisioned IOPS (io1/io2)**: Up to 80,000 IOPS for io2
- **Storage Scaling**: Automatic storage scaling available
- **Backup Storage**: 100% of allocated storage free

### **Cost Structure (ap-southeast-5)**
- **db.t3.micro**: $0.018/hour (~$13/month)
- **db.t3.small**: $0.036/hour (~$26/month)
- **db.r6g.large**: $0.126/hour (~$91/month)
- **Storage (gp3)**: $0.138/GB/month
- **Multi-AZ**: 2x instance cost + storage replication

---

## 2. Amazon Aurora PostgreSQL

### **Architecture**
- **Cloud-Native**: Distributed storage layer across 3 AZs
- **Compute**: Writer instance + up to 15 reader instances
- **Storage**: Auto-scaling from 10GB to 128TB
- **Replication**: Sub-10ms replica lag within region

### **Key Advantages**
- **Performance**: Up to 3x faster than standard PostgreSQL
- **Availability**: 99.99% SLA, automatic failover in 30 seconds
- **Durability**: 6-way replication across 3 AZs
- **Global Database**: Cross-region replication with <1 second lag

### **Unique Features**
- **Aurora ML**: Native integration with SageMaker and Comprehend
- **Parallel Query**: Faster analytics on large datasets
- **Fast Clone**: Create database copies in minutes
- **Backtrack**: Rewind database to previous point in time

### **Cost Structure (ap-southeast-5)**
- **db.r6g.large**: $0.252/hour (~$182/month)
- **Storage**: $0.12/GB/month (pay for used space only)
- **I/O Requests**: $0.24/million requests
- **Backup Storage**: $0.024/GB/month beyond free tier

### **Aurora Serverless v2**
- **Auto-scaling**: 0.5 to 128 ACUs (Aurora Capacity Units)
- **ACU Pricing**: $0.18/ACU/hour
- **Scaling**: Adjusts capacity in seconds based on workload
- **Minimum Cost**: ~$65/month (0.5 ACU always-on)

---

## 3. RDS Proxy

### **Purpose**
Connection pooling and management for applications with high connection counts or short-lived connections.

### **Benefits**
- **Connection Pooling**: Reduces database connection overhead
- **Failover**: Faster failover times (< 30 seconds)
- **Security**: IAM authentication, Secrets Manager integration
- **Scaling**: Supports up to 100,000 connections

### **Cost**
- **RDS Proxy**: $0.021/hour per vCPU of target instance
- **Example**: For db.r6g.large (2 vCPUs) = $0.042/hour (~$30/month)

---

## Performance Characteristics

### **RDS PostgreSQL Performance**
- **IOPS**: Depends on storage type (3K-80K IOPS)
- **Connections**: Up to 5,000 concurrent connections
- **Memory**: Instance-dependent (1.5GB to 768GB)
- **CPU**: 1-128 vCPUs available

### **Aurora PostgreSQL Performance**
- **Read Scaling**: Up to 15 read replicas
- **Write Performance**: Distributed storage layer optimization
- **Connection Limits**: Up to 5,000 connections per instance
- **Query Performance**: Parallel query for analytics workloads

### **Benchmarking (db.r6g.large)**
| Metric | RDS PostgreSQL | Aurora PostgreSQL |
|--------|----------------|-------------------|
| **Max IOPS** | 12,000 (io2) | ~13,000 |
| **Read Replicas** | 5 | 15 |
| **Failover Time** | 60-120 seconds | 30 seconds |
| **Cross-AZ Lag** | Variable | <10ms |

---

## High Availability & Disaster Recovery

### **RDS Multi-AZ**
- **Synchronous Replication**: To standby instance in different AZ
- **Automatic Failover**: DNS endpoint switching
- **Maintenance**: Zero-downtime patching
- **RPO**: Near-zero data loss
- **RTO**: 60-120 seconds

### **Aurora High Availability**
- **Built-in Multi-AZ**: 6-way replication across 3 AZs
- **Automatic Failover**: 30-second failover to read replica
- **Self-Healing Storage**: Automatic repair of data blocks
- **RPO**: Typically <1 second
- **RTO**: 30 seconds

### **Backup Strategies**
- **Automated Backups**: 1-35 day retention period
- **Manual Snapshots**: User-initiated, kept until deleted
- **Point-in-Time Recovery**: Restore to any second within retention period
- **Cross-Region Backups**: For disaster recovery scenarios

---

## Security Features

### **Encryption**
- **At Rest**: AES-256 encryption using AWS KMS
- **In Transit**: SSL/TLS encryption enforced
- **Key Management**: Customer-managed or AWS-managed KMS keys
- **Transparent**: No application changes required

### **Access Control**
- **IAM Database Authentication**: Token-based authentication
- **VPC Security**: Deploy in private subnets
- **Security Groups**: Network-level access control
- **Parameter Groups**: Database configuration management

### **Compliance**
- **Certifications**: SOC, PCI DSS, HIPAA, FedRAMP
- **Auditing**: Database activity streams to Kinesis
- **Monitoring**: Performance Insights, CloudWatch integration

---

## Cost Optimization Strategies

### **Instance Right-Sizing**
- **CPU Utilization**: Target 70-85% average utilization
- **Memory Usage**: Monitor for memory pressure
- **Connection Patterns**: Use RDS Proxy for high-connection scenarios
- **Burstable Instances**: T3/T4g for variable workloads

### **Storage Optimization**
- **gp3 Storage**: More cost-effective than gp2 for most workloads
- **Storage Auto-scaling**: Avoid manual storage management
- **Aurora**: Pay only for used storage vs. pre-allocated
- **Compression**: Enable table compression for large datasets

### **Reserved Instances**
- **1-Year Terms**: ~40% savings over on-demand
- **3-Year Terms**: ~60% savings over on-demand
- **Instance Flexibility**: Size flexibility within instance family
- **Payment Options**: No upfront, partial upfront, all upfront

---

## Decision Framework

### **Choose RDS PostgreSQL When:**
- **Predictable Workloads**: Steady, known resource requirements
- **Cost Sensitivity**: Lower baseline costs important
- **Simple Architecture**: Single primary with read replicas sufficient
- **Existing Tools**: Current PostgreSQL tools and processes
- **Storage Flexibility**: Need specific storage configurations

### **Choose Aurora PostgreSQL When:**
- **High Availability**: 99.99% SLA requirement
- **Performance**: Need 3x PostgreSQL performance improvement
- **Global Applications**: Cross-region replication required
- **Variable Workloads**: Auto-scaling storage beneficial
- **Modern Features**: ML integration, parallel query needed

### **Choose Aurora Serverless v2 When:**
- **Intermittent Workloads**: Development, testing, or sporadic production
- **Unpredictable Traffic**: Automatic scaling required
- **Cost Optimization**: Pay only for actual capacity used
- **Rapid Scaling**: Need second-level scaling response

### **Add RDS Proxy When:**
- **High Connection Count**: >1,000 concurrent connections
- **Lambda Functions**: Serverless applications with connection limits
- **Connection Pooling**: Application doesn't handle pooling well
- **Failover Speed**: Need faster failover than native options

---

## eTR+ Pipeline Integration

### **Operations Database Role**
- **Metadata Storage**: DAG runs, task status, data lineage
- **Configuration Management**: Pipeline parameters, connection strings
- **Quality Metrics**: Data quality check results and trends
- **User Management**: Access control, audit logs

### **Recommended Architecture for eTR+**
```sql
-- Example schema for operations database
CREATE SCHEMA pipeline_ops;
CREATE SCHEMA data_quality;
CREATE SCHEMA audit_logs;

-- Pipeline execution tracking
CREATE TABLE pipeline_ops.dag_runs (
    run_id UUID PRIMARY KEY,
    dag_id VARCHAR(255),
    execution_date TIMESTAMP,
    state VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Data quality metrics
CREATE TABLE data_quality.check_results (
    check_id UUID PRIMARY KEY,
    table_name VARCHAR(255),
    check_type VARCHAR(100),
    result_value NUMERIC,
    passed BOOLEAN,
    checked_at TIMESTAMP DEFAULT NOW()
);
```

### **Connection Patterns**
- **Airflow Metadata**: Primary workload for DAG execution state
- **Application Connections**: Short-lived connections from Lambda/ECS
- **Analytics Queries**: Read replicas for reporting dashboards
- **Batch Updates**: Bulk data quality result inserts

---

## Regional Availability (Malaysia ap-southeast-5)

| Service | Available | Launch Date | Notes |
|---------|-----------|-------------|--------|
| **RDS PostgreSQL** | ✅ Yes | August 2024 | All instance types available |
| **Aurora PostgreSQL** | ✅ Yes | August 2024 | Full feature set |
| **Aurora Serverless v2** | ✅ Yes | August 2024 | Auto-scaling available |
| **RDS Proxy** | ✅ Yes | August 2024 | Connection pooling supported |
| **Performance Insights** | ✅ Yes | August 2024 | Monitoring included |

### **Data Sovereignty Compliance**
- **Data Residency**: All data remains in ap-southeast-5
- **Backup Storage**: Automated backups stored in same region
- **Cross-Region**: Optional for disaster recovery only
- **Compliance**: Meets local data protection requirements

---

## Monitoring & Maintenance

### **Key Metrics to Monitor**
- **CPU Utilization**: Target 70-85% average
- **Database Connections**: Monitor for connection exhaustion
- **Read/Write IOPS**: Ensure storage can handle workload
- **Replication Lag**: For read replicas and Multi-AZ
- **Buffer Cache Hit Ratio**: Should be >95%

### **Maintenance Windows**
- **Automatic**: Minor version updates during maintenance window
- **Blue/Green**: Zero-downtime major version upgrades
- **Scheduling**: Configure for low-traffic periods
- **Testing**: Always test upgrades in non-production first

### **Backup Verification**
- **Automated Testing**: Restore to test environment regularly
- **Recovery Procedures**: Document and test disaster recovery
- **Retention Policies**: Balance cost with recovery requirements
- **Cross-Region**: For critical production workloads