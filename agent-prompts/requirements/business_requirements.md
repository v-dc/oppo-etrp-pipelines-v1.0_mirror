# CTOS eTR+ Business Requirements Document

## Executive Summary
Rebuild the CTOS eTR+ (enhanced Trade Reference Plus) platform to handle significant growth in BNPL (Buy Now Pay Later) data submissions driven by the Consumer Credit Act (CCA) 2025 regulatory requirements, while creating a scalable, automated, and quality-driven solution on AWS.

## Business Context

### Regulatory Driver
- **Consumer Credit Act (CCA) 2025**: Effective December 2025, mandates BNPL reporting to licensed CRA
- **Grace Period**: 6-month grace period to start reporting (June 2026 compliance target)
- **Impact**: Expected 2x growth in contributors (35→70 entities) and 4-5x growth in records (700K→2.8-3.5M monthly)

### Current State Challenges
- **Infrastructure at Capacity**: On-premise server already at memory limits with current volumes
- **Scalability Issues**: Memory-intensive pandas processing cannot handle projected growth
- **Architecture Debt**: 143 database tables with only 4 final tables, no UAT/production separation
- **Manual Operations**: High analyst workload for exception handling and data quality issues

## Business Objectives

### Primary Goals
1. **Create Best Practice eTR+ Solution**: Modern AWS-based architecture following cloud-native patterns
2. **Promote Automation**: Reduce operational overhead and enable scalability for 5x data growth
3. **Improve Data Quality**: Implement demonstrable framework with KPIs, dashboards, and reports
4. **Operational Efficiency**: Create dashboards to reduce analyst ad-hoc work and manual interventions
5. **Enable Innovation**: Support new product development capabilities through calculated variables/features

### Success Metrics

#### Operational Performance
- **Processing Scalability**: Handle projected 5x volume increase (2.8-3.5M monthly records)
- **Processing Speed**: Improve end-to-end pipeline performance 
- **Error Reduction**: Decrease data quality issues and manual interventions
- **System Availability**: Maintain high uptime for production processing

#### Business Impact
- **Regulatory Compliance**: Meet CCA 2025 implementation requirements by December 2025
- **Contributor Growth**: Support expected 2x contributor growth (35→70 entities) 
- **Volume Handling**: Process projected 4-5x record growth (700K→2.8-3.5M monthly)
- **Data Quality**: Implement measurable quality framework with automated reporting
- **Attribute Engine**: Enable calculated characteristics for enhanced credit reporting capabilities

#### Technical Excellence
- **Automation**: Reduce manual operations and analyst intervention
- **Monitoring**: Real-time operational dashboards for pipeline health and data quality
- **Scalability**: Architecture supporting projected growth requirements

## Stakeholders

### Internal CTOS Teams
- **Data Engineering Team**: Primary system users for data processing and quality management
- **Business Operations**: Contributor relationship management and exception handling
- **Analytics Team**: Data consumers for analysis and reporting
- **IT Infrastructure**: AWS environment management and security compliance

### External Stakeholders
- **BNPL Contributors**: 35+ current entities with expected growth to 70+ entities
- **Regulatory Bodies**: Compliance with CCA 2025 and related financial regulations
- **Credit Enquiry Clients**: End consumers of processed credit data and reports

## Functional Requirements

### Data Processing Capabilities
1. **Multi-Source Ingestion**: Support SFTP, API, and web portal submission methods
2. **Flexible Data Formats**: Handle both fixed payment (41-column) and varying payment templates
3. **Real-Time Processing**: Process contributor data within defined SLA windows
4. **Exception Management**: Automated issue detection with JIRA integration for resolution tracking
5. **Data Validation**: Comprehensive quality checking using Great Expectations framework

### Contributor Management
1. **Scalable Onboarding**: Support rapid onboarding of new BNPL contributors
2. **Layout Flexibility**: Handle contributor-specific data layouts and transformations
3. **Submission Methods**: Maintain current SFTP while adding B2B API capabilities
4. **Data Correction**: Efficient resubmission and patching processes for quality issues

### Operational Features
1. **Automated Workflows**: End-to-end processing with minimal manual intervention
2. **Quality Monitoring**: Real-time data quality dashboards and alerting
3. **Audit Trail**: Complete transaction and processing history for compliance
4. **Error Recovery**: Robust handling of processing failures with automated retry logic

### Analytics and Reporting
1. **Attribute Generation Engine**: Calculate characteristics on top of raw data loaded in database
   - On-demand calculation for live credit report requests
   - Batch calculation for retrospective enquiries
   - Persistence strategy to be determined in design phase (most attributes calculated on-demand)
2. **Operational Dashboards**: Real-time monitoring of pipeline health and performance
3. **Data Quality Reports**: Automated generation of quality metrics and trend analysis
4. **Historical Analysis**: Support for time-series analysis and trend calculations

## Non-Functional Requirements

### Performance Requirements
- **Processing Volume**: Handle 2.8-3.5M monthly records (5x current volume)
- **Processing Speed**: Complete daily processing within 4-hour SLA window
- **Concurrent Processing**: Support multiple contributor files processing simultaneously
- **Resource Efficiency**: Optimize memory usage and processing costs on AWS

### Scalability Requirements
- **Horizontal Scaling**: Auto-scaling capabilities to handle variable workloads
- **Storage Growth**: Support petabyte-scale data growth over 5-year horizon
- **Contributor Growth**: Architecture supports 100+ contributors without major redesign
- **Feature Expansion**: Extensible framework for new calculated variables and products

### Reliability Requirements
- **System Availability**: 99.5% uptime during business hours
- **Data Durability**: Zero data loss tolerance with comprehensive backup and recovery
- **Processing Reliability**: 99% successful processing rate for quality data submissions
- **Disaster Recovery**: Recovery Point Objective (RPO) of 4 hours, Recovery Time Objective (RTO) of 2 hours

### Security and Compliance
- **Data Residency**: All processing and storage within Malaysia region (AWS ap-southeast-1)
- **Encryption**: Data encrypted at rest and in transit using AWS KMS
- **Access Control**: Role-based access with audit logging for all data access
- **Regulatory Compliance**: GDPR compliance for personal data and local financial regulations

## Current State Analysis

### Existing Infrastructure Limitations
- **Platform**: On-premise server with memory-intensive pandas processing
- **Capacity**: Already at limits with current 700K monthly records
- **Architecture**: 143 database tables with only 4 final tables indicating architectural debt
- **Scalability**: Cannot handle projected 5x growth without complete rebuild

### Data Volume Profile
- **Current Contributors**: 35 entities (1 with varying layout not loaded)
- **Top Contributors**: 9 contributors account for 91% of records
  - **JCL**: 38% of records (largest contributor)
  - **Boost**: 12% of records (added October 2024)
- **Business Mix**: 32% from motor financing, expected to shift with BNPL growth
- **Data Quality**: Top contributors have better recency (1.2 vs 1.6 months average lag)

### Current Process Flow Assessment
- **SFTP Download**: Automated but limited scalability
- **Individual Processing**: Contributor-specific transformations create maintenance overhead
- **Quality Validation**: Great Expectations framework in place but needs enhancement
- **Exception Handling**: Manual processes via Teams and JIRA need automation
- **Database Loading**: Multi-table MySQL approach needs simplification

## Business Value Proposition

### Immediate Benefits
- **Regulatory Readiness**: Ensure compliance with CCA 2025 requirements
- **Operational Efficiency**: Reduce manual work and analyst intervention by 70%
- **Quality Improvement**: Implement measurable data quality framework
- **Cost Optimization**: AWS cloud economics vs. on-premise infrastructure scaling

### Strategic Advantages
- **Competitive Position**: Market-leading BNPL data processing capabilities
- **Innovation Platform**: Foundation for new product development and features
- **Scalability**: Support business growth without major system redesigns
- **Automation**: Free up analyst resources for higher-value activities

## Project Scope

### Phase I: Infrastructure and Core Processing (Months 1-3)
- AWS infrastructure setup and security configuration
- Core data ingestion pipelines with auto-scaling
- Basic data validation and quality framework
- Migration of critical contributor processing

### Phase II: Advanced Features and Integration (Months 4-6)
- Enhanced quality monitoring and operational dashboards
- Advanced feature engineering and calculated variables
- Complete contributor migration and testing
- Integration with existing systems and workflows

### Phase III: Optimization and Launch (Months 7-9)
- Performance optimization and cost management
- Comprehensive testing and disaster recovery validation
- User training and documentation
- Production launch and monitoring

### Out of Scope
- Migration of historical data beyond operational requirements
- Changes to external contributor submission formats
- Integration with systems outside CTOS eTR+ domain

## Risk Assessment

### Technical Risks
- **AWS Migration Complexity**: Mitigation through phased approach and proof-of-concept validation
- **Data Quality Issues**: Mitigation through comprehensive validation framework and contributor engagement
- **Performance Under Load**: Mitigation through load testing and auto-scaling configuration

### Business Risks
- **Regulatory Timeline**: CCA 2025 implementation pressure; mitigation through aggressive Phase I timeline
- **Contributor Readiness**: BNPL entities may struggle with technical integration; mitigation through early engagement
- **Resource Availability**: Technical team capacity; mitigation through clear prioritization and external support

### Operational Risks
- **System Transition**: Risk of processing disruption; mitigation through parallel running and rollback procedures
- **User Adoption**: Resistance to new processes; mitigation through training and change management
- **Cost Overrun**: AWS costs exceed projections; mitigation through cost monitoring and optimization

## Assumptions and Dependencies

### Key Assumptions
- **AWS Region**: ap-southeast-1 (Malaysia) provides required compliance and performance
- **Contributor Growth**: 2x contributor growth materializes as projected
- **Volume Growth**: 4-5x record volume growth occurs within 12-month timeframe
- **Team Capacity**: Current team can be trained on AWS technologies within project timeline

### Critical Dependencies
- **AWS Account Setup**: Organizational approval and account provisioning
- **Contributor Engagement**: Active participation in testing and validation phases
- **Regulatory Clarity**: Final CCA 2025 implementation guidelines from authorities
- **Budget Approval**: Sufficient funding for AWS infrastructure and development resources

## Acceptance Criteria

### Minimum Viable Product (MVP)
- [ ] Successfully process current 35 contributors with no data loss
- [ ] Handle 2.8M monthly records with 4-hour SLA compliance
- [ ] Implement automated quality validation with Great Expectations
- [ ] Deploy operational dashboards for pipeline monitoring
- [ ] Achieve 99% automated processing with minimal manual intervention

### Quality Gates
- [ ] Zero data loss during production cutover
- [ ] 99.5% system availability during business hours
- [ ] 70% reduction in analyst manual intervention hours
- [ ] Complete audit trail for all data processing and access
- [ ] Successful disaster recovery validation within RTO/RPO targets

### Business Outcomes
- [ ] Full compliance readiness for CCA 2025 by December 2025
- [ ] Support for 70+ contributors without performance degradation
- [ ] Operational cost reduction of 30% compared to scaling current infrastructure
- [ ] Foundation in place for new product feature development
- [ ] Measurable improvement in data quality metrics and contributor satisfaction

---

**Document Owner**: CTOS Data Engineering Team  
**Last Updated**: July 2025  
**Review Frequency**: Monthly during project execution  
**Approval Required**: CTOS Technical Leadership and Business Operations