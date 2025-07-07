# CB-Core Data Paths Architecture

## Overview
CB-Core data processing uses specific directory paths for different types of data and processing stages.

## Data Directory Structure

### Historical Data (Read-Only)
```
/data1/systems/cb-system/data/raw/
├── [19,976 historical credit bureau files]
├── Format: {PROVIDER}_{PERIOD}_{TIMESTAMP}_{SEQUENCE}.txt
├── Examples:
│   ├── BK00001_199902_20250115_0930_01.txt
│   ├── OT00005_202412_20250116_0946_25.txt
│   └── MG00001_202411_20250116_1015_15.txt
└── Access: Historical processing pipeline only
```

### Live Data (Active Processing)
```
/data1/systems/cb-system/data/raw-incoming/
├── [New files arrive here for processing]
├── Format: Same as historical files
├── Processing: Real-time ingestion pipeline
└── Lifecycle: Files processed → moved to processed/
```

### Processed Archive
```
/data1/systems/cb-system/data/processed/
├── historical/
│   └── [Completed historical files]
├── live/
│   └── [Completed live files]
└── quarantine/
    └── [Files with processing issues]
```

### Reference Data (Read-Only)
```
/data1/systems/cb-system/data/raw-dictionary/
├── dictionary_fields_final.csv      # Field definitions
├── institution_final.csv            # Institution lookup
├── raw-filename-parse.txt           # Filename format spec
└── Access: Reference only, copied to cb-core/docs/dictionaries/
```

## Storage Systems

### Iceberg Warehouse (Staging)
```
/data2/systems/data/jdbc_warehouse/
├── default/                         # Default namespace
│   ├── cb_raw_data/                # Raw ingested data
│   ├── cb_quality_metrics/         # Data quality tracking
│   └── cb_processing_audit/        # Processing audit trail
├── Catalog: PostgreSQL jdbc_catalog_db
├── Purpose: Complete data staging with quality flags
└── Access: Spark applications via JDBC catalog
```

### PostgreSQL Operational (Clean Data)
```
Database: boards (192.168.0.74:5432)
Tables:
├── loans_current                    # Current loan states
├── institution_performance          # Institution metrics
├── data_quality_summary             # Quality monitoring
└── geographic_analysis              # Geographic breakdowns
Purpose: Clean operational data for analytics/reporting
Access: PostgreSQL connections, Metabase dashboards
```

## File Processing Flow

### Historical Processing Path
```
/data1/systems/cb-system/data/raw/
    ↓ [Spark Processing]
/data2/systems/data/jdbc_warehouse/ (Iceberg Staging)
    ↓ [Quality Validation & Manual Corrections]
PostgreSQL boards database (Clean Data)
    ↓ [Archive]
/data1/systems/cb-system/data/processed/historical/
```

### Live Processing Path
```
/data1/systems/cb-system/data/raw-incoming/
    ↓ [Real-time Spark Processing]
/data2/systems/data/jdbc_warehouse/ (Iceberg Staging)
    ↓ [Quality Validation & Manual Corrections]
PostgreSQL boards database (Clean Data)
    ↓ [Archive]
/data1/systems/cb-system/data/processed/live/
```

## Access Patterns

### By System Component

#### Spark Jobs
- **Read**: `/data1/systems/cb-system/data/raw/` (historical)
- **Read**: `/data1/systems/cb-system/data/raw-incoming/` (live)
- **Write**: `/data2/systems/data/jdbc_warehouse/` (Iceberg)
- **Write**: PostgreSQL boards database

#### Airflow DAGs
- **Monitor**: `/data1/systems/cb-system/data/raw-incoming/` (file detection)
- **Orchestrate**: Spark job execution
- **Archive**: Move files to `/data1/systems/cb-system/data/processed/`

#### Great Expectations
- **Validate**: Data in Iceberg warehouse
- **Report**: Quality metrics to PostgreSQL
- **Quarantine**: Problem files to `/data1/systems/cb-system/data/processed/quarantine/`

### By Processing Mode

#### Live Mode (Default Active)
- **Monitor**: `/data1/systems/cb-system/data/raw-incoming/`
- **Process**: Files as they arrive
- **Archive**: `/data1/systems/cb-system/data/processed/live/`

#### Historical Mode (Manual Activation)
- **Process**: `/data1/systems/cb-system/data/raw/`
- **Batch**: Configurable date ranges
- **Archive**: `/data1/systems/cb-system/data/processed/historical/`

## File Lifecycle Management

### Successful Processing
1. **Detection**: File appears in source directory
2. **Validation**: Schema and format checks
3. **Processing**: Spark transformation and quality checks
4. **Staging**: Load to Iceberg with quality flags
5. **Review**: Manual corrections if needed
6. **Operational**: Load clean data to PostgreSQL
7. **Archive**: Move to processed directory

### Failed Processing
1. **Detection**: File processing failure
2. **Quarantine**: Move to quarantine directory
3. **Analysis**: Manual review of issues
4. **Correction**: Fix data or processing logic
5. **Reprocess**: Return to normal processing flow

## Permissions and Security

### File System Permissions
- **CB-Core Application**: Read/write access to all CB-System data paths
- **Spark Jobs**: Execute as CB-Core application user
- **Airflow**: Execute as CB-Core application user

### Database Permissions
- **Iceberg Catalog**: `jdbc_user` with read/write to jdbc_catalog_db
- **Operational Database**: `spark_user` with read/write to boards database

## Monitoring and Operations

### Disk Space Monitoring
- **Critical**: `/data1/systems/cb-system/data/` (processing and archive)
- **Critical**: `/data2/systems/data/jdbc_warehouse/` (Iceberg storage)
- **Watch**: Growth rates during historical processing

### Performance Considerations
- **Historical Processing**: Sequential to avoid I/O bottlenecks
- **Live Processing**: Real-time with small batch sizes
- **Archive Strategy**: Regular cleanup of old processed files

## Configuration for Development

### Environment Variables
```bash
# CB-Core data paths
export CB_DATA_ROOT="/data1/systems/cb-system/data"
export CB_RAW_HISTORICAL="$CB_DATA_ROOT/raw"
export CB_RAW_INCOMING="$CB_DATA_ROOT/raw-incoming"
export CB_PROCESSED="$CB_DATA_ROOT/processed"
export CB_WAREHOUSE="/data2/systems/data/jdbc_warehouse"
```

### Spark Configuration References
```python
# Use in Spark applications
RAW_HISTORICAL_PATH = "/data1/systems/cb-system/data/raw"
RAW_INCOMING_PATH = "/data1/systems/cb-system/data/raw-incoming"
PROCESSED_PATH = "/data1/systems/cb-system/data/processed"
WAREHOUSE_PATH = "/data2/systems/data/jdbc_warehouse"
```

This data architecture supports both the current single-server implementation and future scaling to distributed cloud environments.
