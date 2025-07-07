# Data Context Document - CB-Core

## Data Sources Overview

### Historical Data Inventory
- **Total Files**: 19,976 files (February 1999 - December 2024)
- **Institution Types**: 123 institutions across 5 categories (BK, MG, LN, FS, OT)
- **File Format**: 63-field pipe-delimited text files
- **Data Integration**: Combined origination + servicing data per record

### Live Data Characteristics
- **Frequency**: Daily arrivals
- **Volume**: ~50 files per month
- **Format**: Same 63-field pipe-delimited structure
- **Processing**: Real-time within 30 minutes of arrival

## File Format Specifications

### Credit Bureau File Structure
- **Origination Fields**: Positions 1-31 (loan application details)
- **Servicing Fields**: Positions 32-63 (monthly performance data)
- **Business Key**: `id_loan` + `period` (unique identifier)
- **Quality Pattern**: High completeness on core fields, sparse on optional fields

### Filename Pattern Analysis
- **Format**: `{PROVIDER}_{PERIOD}_{DATE}_{TIME}_{SECONDS}.txt`
- **Example**: `BK00001_199902_19990325_0930_20.txt`
- **Components**:
  - `BK00001`: Provider code (6 chars: 2 letters + 5 digits)
  - `199902`: Reference period (YYYYMM)
  - `19990325`: Date (YYYYMMDD)
  - `0930`: Time (HHMM)
  - `20`: Seconds (2 digits)
- **Regex**: `^([A-Z]{2}\\d{5})_(\\d{6})_(\\d{8})_(\\d{4})_(\\d{2})\\.txt$`

### Data Schema Reference
Based on `dictionary_fields_final.csv` with 63 fields:

#### Key Fields (Examples)
- **fico**: Numeric, 4 length, origination data
- **dt_first_pi**: Date, 6 length, origination data
- **orig_upb**: Numeric, 12 length, origination data
- **id_loan**: Alpha, 12 length, servicing data
- **period**: Date, 6 length, servicing data
- **curr_act_upb**: Numeric, 12,2 length, servicing data

#### Data Types
- **Numeric**: Integer and decimal fields
- **Alpha**: Text/character fields
- **Date**: YYYYMM or YYYYMMDD format
- **Alpha Numeric**: Mixed character and number fields

## Data Quality Characteristics

### Quality Patterns Observed
- **Core Fields**: High completeness (>95%)
- **Optional Fields**: Variable completeness (20-80%)
- **Referential Integrity**: Provider codes consistent
- **Temporal Consistency**: Period progression logical

### Quality Validation Requirements
- **Schema Conformance**: 63 fields present and correctly typed
- **Data Type Validation**: Numeric ranges, date formats, text patterns
- **Required Field Presence**: Core fields must not be null
- **Value Range Checks**: FICO scores (300-850), DTI ratios (0-100%)
- **Format Validation**: Date formats, provider code patterns

### Quality Scoring Approach
- **Score Range**: 0-100 based on validation results
- **Validation Results**: Complete Great Expectations output stored
- **Quality Flags**: PASSED, FAILED, CORRECTED status indicators
- **Correction History**: Audit trail of all manual corrections

## File Processing Flows

### File Lifecycle Management

#### Successful Processing Flow
1. **Detection**: File appears in source directory
2. **Validation**: Schema and format checks
3. **Processing**: Spark transformation and quality checks
4. **Staging**: Load to Iceberg with quality flags
5. **Review**: Manual corrections if needed
6. **Operational**: Load clean data to PostgreSQL
7. **Archive**: Move to processed directory

#### Failed Processing Flow
1. **Detection**: File processing failure
2. **Quarantine**: Move to `/data1/systems/cb-system/data/processed/quarantine/`
3. **Analysis**: Manual review of issues
4. **Correction**: Fix data or processing logic
5. **Reprocess**: Return to normal processing flow

### Processing Path by Mode

#### Historical Processing Path
```
/data1/systems/cb-system/data/raw/
    ↓ [Spark Processing with historical profile]
/data2/systems/data/jdbc_warehouse/ (Iceberg Staging)
    ↓ [Quality Validation & Manual Corrections]
PostgreSQL boards database (Clean Data)
    ↓ [Archive]
/data1/systems/cb-system/data/processed/historical/
```

#### Live Processing Path
```
/data1/systems/cb-system/data/raw-incoming/
    ↓ [Real-time Spark Processing with live profile]
/data2/systems/data/jdbc_warehouse/ (Iceberg Staging)
    ↓ [Quality Validation & Manual Corrections]
PostgreSQL boards database (Clean Data)
    ↓ [Archive]
/data1/systems/cb-system/data/processed/live/
```

### Access Patterns by System Component

#### Spark Jobs
- **Read Historical**: `/data1/systems/cb-system/data/raw/` (19,976 files)
- **Read Live**: `/data1/systems/cb-system/data/raw-incoming/` (new files)
- **Read Reference**: `/data1/systems/cb-system/data/raw-dictionary/` (metadata)
- **Write Staging**: `/data2/systems/data/jdbc_warehouse/` (Iceberg)
- **Write Operational**: PostgreSQL boards database (clean data)
- **Archive**: `/data1/systems/cb-system/data/processed/[mode]/`

#### Airflow DAGs
- **Monitor**: `/data1/systems/cb-system/data/raw-incoming/` (file detection)
- **Orchestrate**: Spark job execution with appropriate profiles
- **Archive**: Move files to processed directories
- **Quarantine**: Problem files to quarantine directory

#### Great Expectations
- **Validate**: Data in Iceberg warehouse staging tables
- **Report**: Quality metrics to PostgreSQL operational database
- **Track**: Validation history and correction audit trail
Applied to both Live and Historical processing:
1. **Primary**: Reference Period (YYYYMM format)
2. **Secondary**: Received Timestamp (from filename)
3. **Tertiary**: Provider Code (tie-breaker)

### Processing Stages
1. **File Discovery**: Catalog and prioritize files
2. **Schema Validation**: Apply 63-field structure
3. **Quality Validation**: Great Expectations rules
4. **Staging Storage**: Iceberg with quality metadata
5. **Manual Corrections**: Review and fix quality issues
6. **Re-validation**: Quality re-check after corrections
7. **Operational Export**: Clean data to PostgreSQL

### Data Transformation Pipeline
```
Raw Files (Pipe-delimited) →
Structured DataFrames (Explicit schema) →
Quality Validated Data (GE results) →
Staged Data (Iceberg + metadata) →
Corrected Data (Manual review) →
Clean Data (PostgreSQL operational)
```

## Data Storage Architecture

### Iceberg Staging Tables
- **Purpose**: Complete data staging with quality metadata
- **Catalog**: JDBC catalog (`jdbc_prod`)
- **Warehouse**: `/data2/systems/data/jdbc_warehouse/`
- **Partitioning**: By provider_type and reference_year
- **Format**: Parquet with Snappy compression

### PostgreSQL Operational Tables
- **Purpose**: Clean operational data for analytics/Metabase
- **Database**: `boards` on 192.168.0.74:5432
- **Content**: Only validated, clean data
- **Schema**: Optimized for analytical queries
- **Updates**: Incremental with upsert capability

### Archive Storage
- **Processed Files**: Moved to `/data1/systems/cb-system/data/processed/`
- **Retention**: Complete file history maintained
- **Organization**: By processing mode (live/historical) and date

## Data Lineage and Metadata

### Metadata Tracking
- **Source Files**: Complete filename and path information
- **Processing Metadata**: Correlation IDs, timestamps, processing status
- **Quality Metadata**: Validation results, quality scores, correction history
- **Data Lineage**: Source to operational database tracking

### Audit Requirements
- **Complete Processing Trail**: Every step documented
- **Quality History**: All validation results preserved
- **Correction Tracking**: Manual changes with timestamps and reasons
- **Performance Metrics**: Processing times and resource usage

## Data Governance

### Access Control
- **Source Data**: Read-only access to raw files
- **Staging Data**: Read/write for processing and corrections
- **Operational Data**: Read-only for business users
- **Metadata**: Controlled access for operations team

### Data Retention
- **Raw Files**: Permanent retention in archive
- **Staging Data**: Retained for audit and reprocessing
- **Operational Data**: Business-defined retention policies
- **Metadata**: Permanent retention for lineage tracking

### Compliance Considerations
- **Data Privacy**: Financial data handling requirements
- **Audit Trail**: Complete processing documentation
- **Data Quality**: Validation and correction procedures
- **Access Logging**: All data access tracked and logged

## Integration Specifications

### Database Connections

#### Iceberg Catalog Configuration
```python
spark = SparkSession.builder \
    .config("spark.sql.catalog.jdbc_prod", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.jdbc_prod.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog") \
    .config("spark.sql.catalog.jdbc_prod.uri", "jdbc:postgresql://localhost:5432/jdbc_catalog_db") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.user", "jdbc_user") \
    .config("spark.sql.catalog.jdbc_prod.jdbc.password", "jdbc_password") \
    .config("spark.sql.catalog.jdbc_prod.warehouse", "/data2/systems/data/jdbc_warehouse") \
    .getOrCreate()
```

#### PostgreSQL Operational Connection
```python
jdbc_url = "jdbc:postgresql://192.168.0.74:5432/boards"
connection_properties = {
    "user": "spark_user",
    "password": "spark_password",
    "driver": "org.postgresql.Driver"
}
```

### Data Processing Patterns
- **Explicit Schemas**: Always define DataFrame schemas
- **Error Handling**: Graceful degradation with quarantine
- **Resource Management**: Optimized for single-node processing
- **Quality Integration**: Embedded validation in processing pipeline