# CTOS eTR+ Data Discovery Document

## Executive Summary
Comprehensive analysis of CTOS eTR+ data sources, volumes, quality characteristics, and processing requirements to support the platform rebuild and 5x growth projection for BNPL regulatory compliance.

## Data Source Analysis

### Current Contributor Profile
```yaml
Total Contributors: 35 active entities
Contributor Types:
  - BNPL Providers: 28 entities (80%)
  - Traditional Lenders: 5 entities (14%)
  - Other Financial Services: 2 entities (6%)

Volume Distribution:
  - Top 9 Contributors: 91% of total records
  - JCL (Largest): 38% of monthly volume
  - Boost (Second): 12% of monthly volume
  - Long Tail: 26 contributors account for 9% of volume

Geographic Distribution:
  - Malaysian Entities: 100%
  - Data Residency: All data must remain in Malaysia
```

### Data Submission Methods
```yaml
Current Methods:
  - SFTP Upload: 35/35 contributors (100%)
  - File Format: Excel and text files
  - Frequency: Monthly submissions
  - Timing: Variable (1st-15th of month)

Future Methods (Planned):
  - B2B API: Batch file upload capability
  - Web Portal: CTOS EFT web portal
  - Real-time API: Future enhancement for large contributors
  
Submission Constraints:
  - No real-time submissions currently supported
  - All submissions remain batch-oriented
  - Customized layouts not supported via B2B API
```

### Data Volume Characteristics

#### Current State (2024)
```yaml
Monthly Records: ~700,000 records
Annual Records: ~8.4 million records
File Characteristics:
  - Average file size: 1-5 MB
  - Maximum file size: 50 MB (JCL)
  - Files per month: 35-40
  - Peak processing: End of month

Top Contributors by Volume:
  1. JCL: 38% (266,000 records/month)
  2. Boost: 12% (84,000 records/month)
  3. Others: 50% (350,000 records/month)
```

#### Projected Growth (2025-2026)
```yaml
Regulatory Driver: Consumer Credit Act (CCA) 2025
Growth Projections:
  - Contributors: 35 → 70 entities (2x growth)
  - Monthly Records: 700K → 2.8-3.5M (4-5x growth)
  - Annual Records: 8.4M → 33.6-42M records

BNPL Impact Analysis:
  - New BNPL Contributors: ~35 additional entities
  - BNPL Volume Projection: 60-70% of total volume
  - Motor Financing: Decrease from 32% to ~15-20%
  - Traditional Lending: Stable at ~15-20%
```

## Data Schema and Structure

### Fixed Payment Template (Primary)
Based on draft_dictionary.xlsx analysis:

#### Core Structure
```yaml
Format: 41-column standardized template
Delimiter: Pipe-separated (|)
Encoding: UTF-8
Record Structure: Fixed schema across all contributors

Field Categories:
  - Identification: 8 fields (customer/sponsor details)
  - Agreement Details: 12 fields (loan terms and conditions)  
  - Financial Information: 10 fields (amounts, limits, payment data)
  - Status and Operations: 6 fields (status codes, operation types)
  - Administrative: 5 fields (dates, reference codes)
```

#### Key Data Fields Analysis
```yaml
Customer Identification:
  - cust_reg_id: Customer registration ID (IC/Passport)
  - cust_name: Customer full name
  - cust_mobile_no: Mobile number for contact
  - cust_email: Email address (optional)

Sponsor/Guarantor:
  - sponsor_reg_id: Guarantor identification
  - sponsor_name: Guarantor full name
  - sponsor_mobile_no: Guarantor contact

Agreement Information:
  - agreement_no: Unique agreement identifier
  - agreement_status: Current status (Active/Closed/Default)
  - agreement_start_date: Agreement inception
  - agreement_end_date: Agreement maturity
  - payment_frequency: Payment schedule (Monthly/Weekly)

Financial Details:
  - limit_amount: Credit limit or loan amount
  - outstanding_amount: Current outstanding balance
  - payment_amount: Regular payment amount
  - last_payment_date: Most recent payment
  - last_payment_amount: Last payment value
```

### Data Types and Formats
```yaml
String Fields (25 fields):
  - Names: VARCHAR(100)
  - IDs: VARCHAR(20)
  - Email: VARCHAR(100)
  - Status codes: VARCHAR(10)

Numeric Fields (10 fields):
  - Amounts: DECIMAL(18,2)
  - Percentages: DECIMAL(5,2)
  - Counts: INTEGER

Date Fields (6 fields):
  - Format: YYYYMMDD (string representation)
  - Validation: Date range checks
  - Business rules: Logical date ordering
```

### Varying Payment Template (Secondary)
```yaml
Status: Limited adoption, development pending
Structure: Version 8 template with flexible payment schedules
Usage: < 5% of current contributors
Future: May increase with complex BNPL products
```

## Data Quality Assessment

### Quality Characteristics Analysis

#### High-Quality Data Sources (Top 9 Contributors)
```yaml
Completeness:
  - Mandatory fields: 98-99% populated
  - Customer identification: 99% complete
  - Financial amounts: 97-99% complete
  - Status fields: 99% complete

Accuracy:
  - Date formats: 95% correct format
  - Numeric precision: 98% within expected ranges
  - Referential integrity: 96% valid lookup values

Timeliness:
  - Average submission lag: 1.2 months
  - On-time submission rate: 85%
  - Data freshness: 92% within SLA
```

#### Data Quality Challenges
```yaml
Common Issues:
  - Missing mobile numbers: 15-20% of records
  - Invalid date formats: 3-5% of date fields
  - Inconsistent name formatting: 10% variation
  - Duplicate agreement numbers: 1-2% occurrence

Contributor-Specific Issues:
  - Smaller contributors: Higher error rates (5-10%)
  - New contributors: Learning curve (20-30% initial error rates)
  - Complex products: More validation failures
```

### Current Quality Validation Process
```yaml
Validation Framework: Great Expectations
Validation Points:
  1. File format validation (structure, encoding)
  2. Data type validation (numeric, date, string)
  3. Mandatory field checks (required fields present)
  4. Business rule validation (custom rules)
  5. Referential integrity (lookup table validation)

Quality Scoring:
  - Score range: 0-100 based on validation results
  - Pass threshold: 85% for automatic processing
  - Manual review: 70-84% scores
  - Rejection: < 70% scores

Exception Handling:
  - JIRA integration for issue tracking
  - Email notifications to contributors
  - Resubmission workflow for corrections
  - Patch application for minor corrections
```

## Processing Requirements Analysis

### Current Processing Flow Assessment
```yaml
Process Steps:
  1. SFTP file retrieval (automated)
  2. Individual raw processing (contributor-specific)
  3. Standard raw processing (41-column standardization)
  4. Data validation (Great Expectations)
  5. Staging database loading
  6. Data patching (corrections)
  7. Operations database loading
  8. Reporting and monitoring

Performance Characteristics:
  - End-to-end processing: 4-8 hours
  - File processing: 5-30 minutes per file
  - Quality validation: 2-10 minutes per file
  - Database loading: 1-2 hours for daily batch
```

### Processing Complexity Factors

#### High Complexity Elements
```yaml
Contributor-Specific Processing:
  - 35 different contributor layouts
  - Custom transformation rules per contributor
  - Varying data quality patterns
  - Different business rules and validation

Data Transformation Requirements:
  - Currency standardization (various formats)
  - Date format normalization
  - Name and address standardization
  - Mobile number formatting
  - Duplicate detection and resolution
```

#### Scalability Challenges
```yaml
Current Limitations:
  - Memory-intensive pandas processing
  - Single-threaded processing bottlenecks
  - File-by-file sequential processing
  - Limited parallel processing capability

5x Volume Impact:
  - Processing time: 4-8 hours → 20-40 hours (unacceptable)
  - Memory usage: Exceeds server capacity
  - Storage requirements: Rapid growth in staging tables
  - Manual intervention: Becomes unmanageable
```

## Target Data Architecture

### Recommended Data Flow Design
```yaml
Ingestion Layer:
  - S3 landing zones with event triggers
  - Standardized file naming conventions
  - Automatic file validation and routing
  - Contributor-specific processing paths

Processing Layer:
  - Distributed Spark processing (AWS Glue)
  - Parallel file processing capabilities
  - Schema evolution support (Iceberg)
  - Incremental processing optimization

Quality Layer:
  - Enhanced Great Expectations validation
  - Real-time quality monitoring
  - Automated correction workflows
  - Quality trend analysis and reporting

Storage Layer:
  - Iceberg tables for analytical workloads
  - PostgreSQL for operational queries
  - Automated data lifecycle management
  - Compression and partitioning optimization
```

### Data Modeling Strategy
```yaml
Iceberg Data Lake:
  - Partitioning: Year/Month/Contributor
  - Schema evolution: Backward compatible changes
  - Time travel: Historical data access
  - Compaction: Daily optimization jobs

PostgreSQL Operations:
  - Normalized schema for real-time queries
  - Materialized views for reporting
  - Indexes optimized for common access patterns
  - Automated maintenance and optimization

Data Catalog:
  - AWS Glue catalog for metadata management
  - Schema registry for version control
  - Data lineage tracking
  - Business glossary integration
```

## Quality Framework Enhancement

### Enhanced Validation Rules
```yaml
Level 1 - Structural Validation:
  - File format compliance (41 columns, pipe-delimited)
  - Character encoding validation (UTF-8)
  - Record count verification
  - File size reasonableness checks

Level 2 - Data Type Validation:
  - Numeric field range validation
  - Date format and range checks
  - String length and character validation
  - Enum value validation against lookup tables

Level 3 - Business Rule Validation:
  - Customer identification format (IC/Passport)
  - Agreement date logical ordering
  - Financial amount reasonableness
  - Status transition validity

Level 4 - Cross-Reference Validation:
  - Duplicate agreement detection
  - Customer consistency across agreements
  - Historical data consistency
  - Contributor-specific business rules
```

### Quality Monitoring Requirements
```yaml
Required Metrics:
  - Processing success rate by contributor
  - Quality score trends over time
  - Error frequency and categorization
  - Processing performance metrics

Dashboard Requirements:
  - Executive summary for business stakeholders
  - Operational details for data engineers
  - Contributor-specific quality reports
  - Trend analysis capabilities

Alerting Requirements:
  - Quality threshold breaches
  - Processing failures or delays
  - Unusual data patterns or volumes
  - System performance issues
```

## Integration Requirements

### External System Integration
```yaml
Contributor Systems:
  - SFTP connectivity (existing)
  - B2B API integration (planned)
  - Web portal submissions (existing)
  - Real-time API (future consideration)

Internal Systems:
  - JIRA for exception management
  - Email systems for notifications
  - Analytics platforms for reporting
  - Credit inquiry systems for data consumption

Monitoring Integration:
  - AWS CloudWatch for infrastructure monitoring
  - Custom metrics for business KPIs
  - Log aggregation and analysis
  - Performance monitoring and alerting
```

### Data Consumer Requirements
```yaml
Analytics Team:
  - SQL access to processed data
  - Historical trend analysis capabilities
  - Data export functionality
  - Custom report generation

Operations Team:
  - Real-time processing status
  - Exception management workflows
  - Data quality monitoring
  - Contributor relationship management

External Clients:
  - Credit inquiry API access
  - Report generation services
  - Data extraction capabilities
  - Audit trail access
```

## Regulatory and Compliance Requirements

### Data Protection Requirements
```yaml
Malaysian Data Residency:
  - All data processing within Malaysia region
  - No cross-border data transfers
  - Local backup and disaster recovery
  - Compliance with local data protection laws

Personal Data Handling:
  - GDPR compliance for data subject rights
  - Data minimization principles
  - Purpose limitation enforcement
  - Consent management (where applicable)

Financial Services Compliance:
  - CCA 2025 specific requirements
  - Central bank reporting obligations
  - Audit trail maintenance (7 years)
  - Data integrity and accuracy standards
```

### Audit and Compliance Framework
```yaml
Audit Trail Requirements:
  - Complete data lineage tracking
  - Processing history and changes
  - User access and activity logs
  - Quality validation results

Compliance Reporting:
  - Automated compliance status reports
  - Data quality metrics for regulators
  - Processing performance statistics
  - Exception and resolution tracking

Data Retention:
  - 7-year retention for financial data
  - Automated archival processes
  - Secure deletion procedures
  - Compliance with legal hold requirements
```

## Risk Assessment and Mitigation

### Data Quality Risks
```yaml
High Risk:
  - Data corruption during migration
  - Quality degradation with 5x volume
  - New contributor onboarding errors
  - Regulatory compliance failures

Medium Risk:
  - Processing performance degradation
  - Integration failures with external systems
  - Data schema evolution challenges
  - Security and access control issues

Low Risk:
  - Storage capacity limitations
  - Network connectivity issues
  - Monitoring and alerting gaps
  - Documentation and training needs
```

### Mitigation Strategies
```yaml
Data Validation:
  - Enhanced Great Expectations framework
  - Multi-stage validation processes
  - Automated quality monitoring
  - Real-time alerting and escalation

Processing Reliability:
  - Distributed processing architecture
  - Automated retry and recovery mechanisms
  - Comprehensive error handling
  - Performance monitoring and optimization

Security and Compliance:
  - End-to-end encryption
  - Role-based access controls
  - Comprehensive audit logging
  - Regular compliance assessments
```

## Recommendations

### Immediate Actions (Pre-Implementation)
1. **Data Profiling**: Conduct comprehensive analysis of historical data quality patterns
2. **Schema Validation**: Validate data dictionary completeness with top contributors
3. **Processing Benchmarks**: Establish baseline performance metrics for comparison
4. **Quality Standards**: Define enhanced quality validation rules and thresholds

### Implementation Priorities
1. **Core Processing Pipeline**: Focus on reliable, scalable data ingestion and transformation
2. **Quality Framework**: Implement comprehensive validation and monitoring
3. **Operational Dashboards**: Provide real-time visibility into processing status
4. **Contributor Onboarding**: Streamline processes for rapid contributor addition

### Success Factors for Implementation
```yaml
Processing Performance Requirements:
  - Handle projected 5x volume increase reliably
  - Complete daily processing within acceptable timeframes
  - Maintain data accuracy and completeness
  - Support concurrent file processing

Data Quality Requirements:
  - Improve quality check coverage and accuracy
  - Reduce manual intervention requirements
  - Provide timely exception resolution
  - Maintain high data accuracy standards

Business Outcome Requirements:
  - Support projected contributor growth (35→70 entities)
  - Handle projected volume growth (700K→3.5M monthly records)
  - Achieve CCA 2025 compliance requirements
  - Enable enhanced credit reporting capabilities through attribute engine
```

---

**Document Owner**: CTOS Data Engineering Team  
**Analysis Date**: July 2025  
**Data Sources**: Current eTR+ system, draft_dictionary.xlsx, contributor feedback  
**Next Review**: Monthly during implementation phases