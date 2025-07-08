# eTRPlus Pipeline Context for AWS Architecture Design

## Overview
eTRPlus is a financial data processing system that handles fixed payment data from multiple contributors through a comprehensive ETL pipeline. The system processes contributor data through standardization, validation, staging, patching, and database loading phases.

## Current Pipeline Architecture

### Main Process Flow
1. **Download Raw File from eFT/SFTP** → 2. **Transformation Raw File** → 3. **Ingestion to Staging** → 4. **Patching in Staging** → 5. **Load Data from Staging to Database** → 6. **Generate DQ Report**

### Detailed Process Breakdown

#### 1. Data Ingestion (SFTP Download)
- **Source**: SFTP server (eft.ctos.com.my:225)
- **Input**: Excel contributor list (`list_ref_comid.xlsx`) containing ref_comid, email, prefix
- **Process**: 
  - Automated file retrieval based on contributor list
  - Dynamic folder structure: `/eTR Plus/{email}`
  - Local storage paths: `/talend_prod/.../raw/{year}/{year_month}/{filename}`
  - Cleanup logic based on copy status (success/failure)

#### 2. Raw File Transformation
- **Sub-processes**:
  - Individual Raw Processing (contributor-specific)
  - Standard Raw Processing (41 columns standardization)
  - Data Cleansing
  - Data Validation

##### Standard Raw Processing Functions:
- **Currency conversion**: Dollar columns to numeric
- **Null handling**: Replace nulls with contributor-specific defaults
- **Date formatting**: Agreement status, lodgement dates
- **Registration ID fixes**: Customer and sponsor registration corrections
- **Field population**: op_code, acc_status, del_reason_code logic
- **Mobile number cleaning**: Format standardization and duplicate handling

##### Data Cleansing:
- Column reordering to fixed schema
- Data type conversions (string, date, dollar, number)
- Whitespace and special character removal
- Null value standardization
- Duplicate removal based on sequential tracking

##### Data Validation:
- **Mandatory field checks**: Operation codes, party types, identification fields
- **Dictionary validation**: Predefined value lists
- **Date validation**: Logical ordering, future date prevention
- **Format validation**: IC formats, character limits, numeric constraints
- **Business rule validation**: Critical custom rules

#### 3. Staging Ingestion
- **Error checking**: Row-level validation for eTR+ submission requirements
- **Data merging**: Master, customer, account, statement, sponsor data integration
- **Key generation**: Unique identifiers (tref_id_plus, customer_key, account_key)
- **Deduplication**: Based on composite keys with latest record priority

##### Data Entity Processing:
- **Master Data**: Key management and relationship mapping
- **Customer Data**: Deduplicated customer records with standardized structure
- **Account Data**: Account-level data with add/delete operation handling
- **Statement Data**: Financial statement processing with parallel transformation
- **Sponsor Data**: Sponsor information with unique sp_id assignment

#### 4. Staging Patching
Multiple patching processes to correct data inconsistencies:
- **JCL Patching**: Account status updates due to limit changes
- **Courts Patching**: Relationship start date corrections (account and statement level)
- **FS Patching**: Instalment amount corrections
- **Null Patching Scripts**:
  - Relationship start date filling using fixed templates
  - Limit value correction from reference data
  - Instalment amount filling from trusted sources
  - Tenure month correction using template data

#### 5. Database Loading (MySQL)
- **Data integrity checks**: Reference table validation
- **Table creation**: Timestamped table generation using SQL templates
- **Chunked loading**: 100,000 row batches for performance
- **Data transformation**: Schema alignment and data type standardization
- **View promotion**: DA and RE view creation for analytics and reporting

##### Database Schema:
- **Tables**: keytbl_jcl_uat, relationship_jcl_uat, acc_stts_jcl_uat, sponsor_jcl_uat
- **Views**: Analytics views (DA) and Reporting Environment views (RE)
- **Time-based filtering**: Last 24 months for performance optimization

#### 6. Data Quality Reporting
- **Reconciliation checks**: Raw vs staging data comparison
- **Quality metrics**: Duplicates, nulls, format violations, extreme values
- **Summary generation**: Comprehensive DQ report compilation
- **Email notification**: Automated report distribution

## Technical Requirements

### Data Characteristics
- **Volume**: Multiple contributors, high-volume financial data
- **Format**: Excel files, fixed 41-column schema for standardization
- **Frequency**: Batch processing with timestamp-based organization
- **Data Types**: Financial amounts, dates, identification numbers, status codes

### Processing Requirements
- **Parallel processing**: Multi-threading for performance optimization
- **Memory management**: Chunked processing for large datasets
- **Error handling**: Comprehensive validation and error tracking
- **Data lineage**: Timestamp-based versioning and tracking

### Integration Points
- **SFTP connectivity**: Secure file transfer protocol
- **Database systems**: MySQL for operational data storage
- **File systems**: Structured folder hierarchies for data organization
- **Email systems**: Automated notification capabilities

## Current Technology Stack Context
- **Language**: Python-based processing
- **Data Processing**: Pandas for DataFrame operations
- **Database**: MySQL with SQLAlchemy for ORM
- **File Formats**: Parquet for intermediate storage, CSV for reporting
- **Parallel Processing**: ThreadPoolExecutor for concurrent operations

## Key Business Rules
- **Operation Codes**: 'A' (Add), 'M' (Modify), 'D' (Delete)
- **Party Types**: 'I' (Individual), 'B' (Business/ROB), 'C' (Company/ROC)
- **Account Status Logic**: Conditional updates based on operation codes
- **SSM Validation**: Fuzzy matching for company/business registration
- **Date Constraints**: Historical data validation, future date prevention

## Data Quality Dimensions
- **Completeness**: Mandatory field validation
- **Accuracy**: Cross-reference validation against master data
- **Consistency**: Format standardization and business rule compliance
- **Timeliness**: Date range validation and currency checks
- **Validity**: Dictionary-based value validation

## Performance Considerations
- **Chunked processing**: 100K record batches
- **Parallel execution**: Multi-threading for independent operations
- **Memory optimization**: Intermediate file storage using Parquet
- **Database optimization**: Indexed keys and time-based partitioning

## Security & Compliance
- **SFTP security**: Secure file transfer protocols
- **Data privacy**: Personal identification handling
- **Audit trails**: Comprehensive logging and timestamp tracking
- **Error isolation**: Separate error handling and rejection processes

## Additional Context from Customer Q&A (May 2025)

### Regulatory Context
- **CCA 2025 Compliance**: New Consumer Credit Act 2025 requiring credit providers to submit consumer credit information to credit bureaus
- **Industry Readiness**: Most adopting wait-and-see approach until Act is officially gazetted (end of 2025)
- **Gap Analysis Needed**: Comprehensive gaps/pain points not yet mapped to CCA 2025 requirements

### Current Scale & Volume
- **Contributors**: 35 total contributors onboarded
  - 34 using fixed payment template
  - 1 using varying payment template (development not started, files stored in talendprod)
- **Historical Database Size**:
  - acc_stts: 24.49 GB
  - keytbl: 0.47 GB
  - relationship: 1.75 GB
  - sponsor: 0.20 GB
- **Data History**: Oldest data from November 2019
- **File Tracking**: Historical file load/rejection catalogue available via log files

### Infrastructure Details
- **Processing Server**: Intel Xeon Platinum 8268 CPU @ 2.90GHz, 8 CPU cores, 60GB RAM
- **Database Server**: Different from processing server
- **Environment**: On-premise infrastructure (not AWS)
- **File Submission**: All contributors currently use EFT/SFTP upload method

### Data Submission Methods
- **Primary Method**: EFT/SFTP file uploads (all current contributors)
- **B2B Alternative**: Batch file upload via B2B API integration
  - No customized layouts supported for B2B
  - Still batch-based, not real-time
- **Web Portal**: CTOS EFT web portal available

### Data Quality & Error Management Process
- **Error Communication**: Teams-based communication between Data Engineering and Business teams
- **Contributor Notification**: Email notifications with walkthrough sessions for clarification
- **Data Correction Approach**:
  - Resubmission of discarded records only (not full files)
  - Non-discarded records loaded in meantime
  - Data patching performed on corrected submissions
  - Many historical issues genuine and exist in contributor internal systems
- **Master DQ Report**: Generated after MySQL loading completion
- **Error Persistence**: Errors may remain in database, with ongoing patching as corrections received

### Payment Template Types
- **Fixed Payments**: 41-column standardized template (primary focus)
- **Varying Payments**: v8 template (limited adoption, development pending)
- **Documentation**: Presentation decks provided to subscribers (e.g., BNPL provider presentations)

### API Integration
- **B2B API**: REST API specification available for bulk submissions
- **Customization Limitation**: Customized layouts not supported for B2B API submissions
- **Batch Processing**: All submissions remain batch-oriented regardless of submission method

### Operational Constraints
- **Resource Constraints**: Industry feedback indicates resource limitations for data submission readiness
- **Regulatory Clarity**: Need for clearer reporting requirements from regulators
- **System Integration**: Contributors discovering internal data quality issues during onboarding