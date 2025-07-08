# eTR+ Pipeline Rebuild - Discovery Context

## Project Overview

### Business Context
- **Client**: CTOS (Credit Reporting Agency in Malaysia)
- **Project**: Rebuild eTR+ (enhanced Trade Reference Plus) platform
- **Timeline**: 9-month project (Phases I-III)
- **Region**: Malaysia (AWS ap-southeast-5)

### Regulatory Drivers
- **Consumer Credit Act (CCA) 2025**: Effective December 2025, mandates BNPL reporting to licensed CRA
- **Grace Period**: 6-month grace period to start reporting
- **Impact**: Significant growth in contributor numbers and record volumes expected

### Business Objectives
1. Create best practice eTR+ solution in AWS
2. Promote automation for operations efficiency and scalability
3. Improve data quality with demonstrable framework (KPIs, dashboards, reports)
4. Create operational dashboards to reduce analyst ad-hoc work
5. Enable new product development capabilities (calculated variables/features)

---

## Current State Assessment

### Infrastructure Limitations
- **Current Platform**: On-premise server with memory-intensive pandas processing
- **Status**: Already at capacity limits with current volumes
- **Architecture Issues**: 143 database tables (only 4 are final tables), no UAT/production separation
- **Programming Approach**: Memory-intensive, difficult to scale

### Data Volume Profile
- **Current Contributors**: 35 entities (1 with varying layout not loaded)
- **Monthly Records**: ~700K records currently ingested
- **Expected Growth**: 
  - Contributors: 2x (70 entities)
  - Records: 4-5x (2.8-3.5M monthly records)

### Contributor Analysis
- **Top 9 Contributors**: Account for 91% of records
- **Largest Contributor**: JCL (38% of records)
- **Second Largest**: Boost (12% of records, added Oct 2024)
- **Business Mix**: 32% from motor financing, expected to change with BNPL growth
- **Data Quality**: Top contributors have better recency/lower lag (1.2 vs 1.6 months)

---

## Current Process Flow (To Be Replaced)

### High-Level Process
```
SFTP Download → Raw Processing → Quality Validation → Staging Load → 
Database Load → Patching → Operations DB → Reporting
```

### Key Process Steps
1. **SFTP File Retrieval**: Automated download from 35+ contributor paths
2. **Individual Raw Processing**: Contributor-specific transformations (41 columns)
3. **Data Validation**: Great Expectations framework for quality checks
4. **Staging Operations**: Multi-table MySQL loading with patching
5. **Exception Handling**: JIRA integration for data quality issues
6. **Attribute Generation**: Calculated features engine
7. **Reporting**: Credit report generation and dashboards

### Current Tech Stack
- **File Transfer**: SFTP server (eft.ctos.com.my:225)
- **Processing**: Python with pandas (memory-intensive)
- **Database**: MySQL with 143 tables
- **Orchestration**: Manual processes with high operational complexity
- **Data Format**: 41-column fixed payment layout

---

## Data Architecture Requirements

### Data Layers (Medallion Architecture)
- **Bronze/Raw**: Original contributor files with minimal processing
- **Silver/Processed**: Cleaned, validated, standardized data
- **Gold/Curated**: Business-ready datasets with calculated attributes

### Data Entities
- **Customer Data**: Individual, business, company profiles
- **Account Data**: Credit account information with relationships
- **Statement Data**: Transaction and payment history (last 5 years focus)
- **Sponsor Data**: Guarantor and sponsor information

### Data Quality Framework
- **Validation Rules**: Mandatory field checks, dictionary validation, date logic
- **Quality Metrics**: Completeness, accuracy, consistency, timeliness
- **Error Handling**: Automated exception processing with JIRA integration
- **Reconciliation**: Raw vs processed data comparison

---

## Technical Requirements

### Scalability Needs
- **Volume**: Handle 4-5x increase in data volume
- **Contributors**: Support doubling of data sources
- **Performance**: Reduce processing time and manual intervention
- **Reliability**: Automated recovery and error handling

### Data Quality Improvements
- **Automated Validation**: Great Expectations framework integration
- **Real-time Monitoring**: Data quality dashboards and alerts
- **Lineage Tracking**: Full data provenance and audit trails
- **Schema Evolution**: Handle varying contributor layouts

### Operational Efficiency
- **Automation**: Reduce manual steps and operational complexity
- **Standardization**: Unified processing approach for all contributors
- **Monitoring**: Operations dashboards for pipeline health
- **Exception Management**: Automated issue detection and routing

---

## Compliance and Governance

### Regulatory Requirements
- **Data Residency**: All processing must remain in Malaysia region
- **Audit Trail**: Complete transaction and access logging
- **Data Protection**: GDPR compliance for personal data
- **Financial Regulations**: Local and international compliance

### Security Requirements
- **Encryption**: At rest and in transit
- **Access Control**: Role-based permissions and audit
- **Data Classification**: Sensitive financial data handling
- **Network Security**: VPC isolation and private connectivity

---

## Integration Points

### External Systems
- **Contributors**: 35+ BNPL entities via SFTP/API
- **JIRA**: Issue tracking and exception management
- **Analytics Team**: Data access for analysis
- **Credit Enquiry Clients**: Report generation consumers

### Internal Systems
- **Operations Database**: PostgreSQL for metadata and orchestration
- **Data Warehouse**: Iceberg tables for analytical queries
- **Monitoring Systems**: Operations and data quality dashboards
- **Attribute Engine**: Calculated features generation

---

## New Capabilities Required

### Feature Engineering
- **Calculated Variables**: New product development capability
- **Real-time Attributes**: Dynamic feature generation
- **Historical Analysis**: Time-series and trend calculations
- **Risk Metrics**: Advanced analytics support

### Enhanced Layouts
- **Varying Payments**: Support for flexible payment structures
- **Customer Limits**: Product limit fields addition
- **Extended Fields**: Additional business-specific attributes

---

## Success Criteria

### Operational Metrics
- **Processing Time**: Reduce end-to-end pipeline duration
- **Error Rates**: Decrease data quality issues and manual interventions
- **Scalability**: Successfully handle 5x volume increase
- **Availability**: 99.9% uptime target

### Business Outcomes
- **Automation**: 80% reduction in manual processing steps
- **Data Quality**: Measurable improvement in accuracy and completeness
- **Time to Market**: Faster onboarding of new contributors
- **Feature Development**: Enable calculated variables and new products

### Technical Goals
- **Cost Optimization**: Efficient AWS resource utilization
- **Performance**: Sub-hour processing for daily loads
- **Monitoring**: Complete visibility into pipeline health
- **Maintainability**: Self-service operations capability

---

## Constraints and Considerations

### Technical Constraints
- **Region Lock**: Must use AWS ap-southeast-5 (Malaysia)
- **Data Sovereignty**: No cross-border data movement
- **Legacy Integration**: Maintain compatibility during transition
- **Resource Limits**: Cost-effective scaling approach

### Operational Constraints
- **Parallel Operations**: Maintain current system during transition
- **Training Requirements**: Team capability development
- **Change Management**: Minimal disruption to current operations
- **Timeline Pressure**: CCA 2025 deadline driving urgency

### Business Constraints
- **Budget Sensitivity**: Cost-effective solution required
- **Risk Tolerance**: Financial services compliance requirements
- **Stakeholder Management**: Multiple internal and external parties
- **Quality Standards**: Zero tolerance for data loss or corruption

---

## Architecture Principles

### AWS Well-Architected Alignment
- **Operational Excellence**: Infrastructure as Code, automated deployment
- **Security**: Defense in depth, least privilege access
- **Reliability**: Multi-AZ deployment, automated backup/recovery
- **Performance Efficiency**: Right-sizing, serverless-first approach
- **Cost Optimization**: Consumption-based pricing, lifecycle management
- **Sustainability**: Efficient resource utilization, regional optimization

### Design Priorities
1. **Scalability First**: Design for 10x growth beyond current projections
2. **Automation Focus**: Minimize manual intervention and operational overhead
3. **Data Quality**: Built-in validation and monitoring at every layer
4. **Cost Efficiency**: Leverage managed services and auto-scaling
5. **Security by Design**: Encryption, access control, and audit from ground up