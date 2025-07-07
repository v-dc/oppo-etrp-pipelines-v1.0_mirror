# Phase 4A: Historical Data Processing Implementation

## Overview
Implement historical data processing pipeline for 19,976 credit bureau files (1999-2024) using AI-agentic development with Claude Code.

**Timeline**: 3-4 days focused development  
**Approach**: Follow Phase 2 flowchart sequence exactly  
**Data Flow**: Raw Files → GE Validation → Spark Processing → Iceberg Staging → Manual Corrections → PostgreSQL Clean Data

## Processing Sequence (From Phase 2 Flowcharts)

### **Step 1: File Discovery & Prioritization**
**Purpose**: Identify and sort historical files for processing  
**Logic**: Sort by ref_period → received → provider (universal priority)

**Success Criteria**:
- [ ] Discover all files in `/data1/systems/cb-system/data/raw/`
- [ ] Parse filename format: `{PROVIDER}_{PERIOD}_{TIMESTAMP}_{SEQUENCE}.txt`
- [ ] Sort by universal priority logic
- [ ] Support configurable date range filtering
- [ ] Handle 19,976+ files efficiently

### **Step 2: Combined Processing (Spark + Great Expectations + Iceberg)**
**Purpose**: Process files with integrated quality validation and staging  
**Logic**: Read → Validate → Add Quality Flags → Write to Iceberg (ALL data)

**Success Criteria**:
- [ ] Read pipe-delimited files (63 fields)
- [ ] Apply credit bureau schema transformation
- [ ] Run Great Expectations validation during processing
- [ ] Calculate quality scores (0-100) per record
- [ ] Add metadata (correlation_id, load_timestamp, quality_flags)
- [ ] Write ALL data to `jdbc_prod.default.cb_raw_data` 
- [ ] Partition by institution_type and period_year
- [ ] Handle processing failures gracefully

### **Step 3: Quality Review & Manual Corrections**
**Purpose**: Enable manual review and correction of quality issues  
**Logic**: Query Iceberg for quality issues → Manual corrections → Re-validate

**Success Criteria**:
- [ ] Query Iceberg for records with quality issues
- [ ] Support manual data corrections in Iceberg
- [ ] Re-run Great Expectations after corrections
- [ ] Update quality flags post-correction
- [ ] Track correction history and audit trail

### **Step 4: Clean Data Export to PostgreSQL**
**Purpose**: Load only validated clean data to operational database  
**Logic**: Read from Iceberg WHERE quality_flag = 'PASSED' → Write to PostgreSQL

**Success Criteria**:
- [ ] Read clean data from Iceberg staging
- [ ] Transform to operational schema
- [ ] Write to PostgreSQL `boards` database tables
- [ ] Support incremental updates
- [ ] Maintain data lineage tracking

### **Step 5: Historical Processing Orchestration**
**Purpose**: Airflow DAG to orchestrate the complete historical pipeline  
**Logic**: Manual trigger → Exclusive mode → Progress tracking → Reporting

**Success Criteria**:
- [ ] Manual trigger only (exclusive processing mode)
- [ ] Configurable date range processing
- [ ] Progress tracking and status reporting
- [ ] Error handling and recovery mechanisms
- [ ] Resource optimization for NPD server
- [ ] Complete audit trail and logging

## Module Structure

### **Module 1: File Discovery Service**
- `src/discovery/historical_file_discovery.py`
- `tests/unit/test_file_discovery.py`

### **Module 2: Combined Processing Engine**
- `src/processing/historical_processor.py`
- `src/quality/integrated_validator.py`
- `src/storage/iceberg_staging.py`
- `tests/integration/test_historical_processing.py`

### **Module 3: Manual Corrections Framework**
- `src/corrections/correction_manager.py`
- `src/quality/revalidation_service.py`
- `tests/unit/test_corrections.py`

### **Module 4: Clean Data Exporter**
- `src/export/postgres_exporter.py`
- `src/transform/operational_transformer.py`
- `tests/integration/test_postgres_export.py`

### **Module 5: Historical Processing DAG**
- `airflow/dags/historical_processing/historical_main_dag.py`
- `airflow/dags/historical_processing/historical_tasks.py`
- `tests/airflow/test_historical_dag.py`

## Overall Success Criteria

### **Functional Requirements**
- [ ] Process all 19,976 historical files successfully
- [ ] Complete pipeline from raw files to clean PostgreSQL data
- [ ] Quality validation and scoring on all records
- [ ] Manual correction capability for quality issues
- [ ] Comprehensive error handling and recovery

### **Performance Requirements**
- [ ] Process historical files within 8-24 hours total time
- [ ] Use maximum 7/8 cores and 26/32GB memory (NPD server limits)
- [ ] Support configurable batch sizes for resource optimization
- [ ] Efficient file discovery and priority processing

### **Quality Requirements**
- [ ] >99% data processing success rate
- [ ] Comprehensive quality scoring (0-100) for all records
- [ ] Complete audit trail of all processing steps
- [ ] Zero data loss during processing
- [ ] Accurate data lineage tracking

### **Operational Requirements**
- [ ] Manual trigger and control of processing
- [ ] Progress monitoring and status reporting
- [ ] Resource usage monitoring and optimization
- [ ] Error alerting and notification
- [ ] Support for processing restart and recovery

## Resource Allocation

### **Spark Configuration**
- **Profile**: `historical` (maximum resource allocation)
- **Executors**: 2 instances × 3 cores × 10GB memory
- **Driver**: 1 core × 6GB memory
- **Total**: 7/8 cores, 26/32GB memory

### **Processing Strategy**
- **Sequential Institution Processing**: Process one institution type at a time
- **Batch Size**: 100-500 files per batch (configurable)
- **Checkpointing**: Save progress every batch for restart capability
- **Error Isolation**: Quarantine failed files for separate processing

## Integration Points

### **Data Sources**
- **Input**: `/data1/systems/cb-system/data/raw/` (19,976 files)
- **Reference**: `/data1/systems/cb-system/data/raw-dictionary/` (metadata)

### **Data Targets**
- **Staging**: `/data2/systems/data/jdbc_warehouse/` (Iceberg)
- **Operational**: PostgreSQL `boards` database (192.168.0.74:5432)
- **Archive**: `/data1/systems/cb-system/data/processed/historical/`

### **System Integration**
- **Airflow**: Orchestration and monitoring
- **Great Expectations**: Quality validation and reporting
- **Spark**: Distributed processing engine
- **PostgreSQL**: Operational data storage

---

**Phase 4A Focus**: Historical data processing pipeline  
**Next Phase**: Phase 4B - Live data processing pipeline  
**Development Method**: AI-agentic with Claude Code  
**Expected Duration**: 3-4 development days