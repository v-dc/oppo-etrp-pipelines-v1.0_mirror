# Credit Bureau Template - Corrected Data Flow Diagrams v1.0

## Overview
Two completely independent processing systems that operate exclusively. Each system has its own data sources, processing pipeline, and operates independently with no overlap.

## 1. Live Processing System (Default Active Mode)

```mermaid
graph TB
    subgraph "Live File Processing Pipeline"
        L1[Live Files Arrive<br/>File Drop Location<br/>Real-time arrivals]
        L2[Airflow Live DAG<br/>File detection & orchestration]
        L3[File Priority Queue<br/>ref_period → received → provider]
        L4[Spark Processing<br/>Maximum 2 jobs]
        L5[Great Expectations<br/>Initial data validation]
        L6[Iceberg Staging<br/>All live data + quality flags]
        L7[Manual Corrections<br/>Applied when needed]
        L8[Great Expectations Re-run<br/>Updated quality statistics]
        L9[PostgreSQL Operational<br/>Clean live data only]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> L6
    L6 --> L7
    L7 --> L8
    L8 --> L9
    L6 --> L9
```

## 2. Historical Processing System (Manual Activation Mode)

```mermaid
graph TB
    subgraph "Historical File Processing Pipeline"
        H1[Historical Files<br/>Historical Archive Folder<br/>Configurable path parameter]
        H2[Airflow Historical DAG<br/>Manual activation only]
        H3[File Priority Queue<br/>ref_period → received → provider]
        H4[Spark Processing<br/>Same 2 jobs when active]
        H5[Great Expectations<br/>Initial data validation]
        H6[Iceberg Staging<br/>All historical data + quality flags]
        H7[Manual Corrections<br/>Applied when needed]
        H8[Great Expectations Re-run<br/>Updated quality statistics]
        H9[PostgreSQL Operational<br/>Historical data integration]
    end
    
    H1 --> H2
    H2 --> H3
    H3 --> H4
    H4 --> H5
    H5 --> H6
    H6 --> H7
    H7 --> H8
    H8 --> H9
    H6 --> H9
```

## 3. Live Processing Detailed Sequence

```mermaid
sequenceDiagram
    participant LiveFiles as Live Files
    participant DropFolder as File Drop Location
    participant LiveDAG as Airflow Live DAG
    participant SparkLive as Spark Jobs (Live)
    participant GE1 as Great Expectations Initial
    participant IcebergLive as Iceberg Staging (Live)
    participant CorrectionsLive as Manual Corrections
    participant GE2 as Great Expectations Re-run
    participant PostgresLive as PostgreSQL (Live)
    
    LiveFiles->>DropFolder: Files arrive continuously
    DropFolder->>LiveDAG: File detection
    LiveDAG->>LiveDAG: Sort by priority (ref_period, received, provider)
    LiveDAG->>SparkLive: Trigger processing
    SparkLive->>GE1: Run validation
    GE1->>IcebergLive: Load all data + quality flags
    
    alt Corrections needed
        IcebergLive->>CorrectionsLive: Manual review and fixes
        CorrectionsLive->>GE2: Re-run validation
        GE2->>IcebergLive: Update quality statistics
    end
    
    IcebergLive->>PostgresLive: Load clean data only
    SparkLive->>LiveDAG: Processing complete
```

## 4. Historical Processing Detailed Sequence

```mermaid
sequenceDiagram
    participant Ops as Operations Team
    participant LiveDAG as Live DAG (Deactivated)
    participant HistFolder as Historical Archive Folder
    participant HistDAG as Historical DAG
    participant SparkHist as Spark Jobs (Historical)
    participant GE1 as Great Expectations Initial
    participant IcebergHist as Iceberg Staging (Historical)
    participant CorrectionsHist as Manual Corrections
    participant GE2 as Great Expectations Re-run
    participant PostgresHist as PostgreSQL (Historical)
    
    Note over LiveDAG: Live system running normally
    
    Ops->>LiveDAG: DEACTIVATE Live DAG completely
    Note over LiveDAG: Live files accumulate, no processing
    
    Ops->>HistDAG: ACTIVATE Historical DAG
    Ops->>HistDAG: Set folder parameter path
    HistDAG->>HistFolder: Scan for historical files
    HistDAG->>HistDAG: Sort by priority (ref_period, received, provider)
    HistDAG->>SparkHist: Trigger processing
    SparkHist->>GE1: Run validation
    GE1->>IcebergHist: Load all historical data + quality flags
    
    alt Corrections needed
        IcebergHist->>CorrectionsHist: Manual review and fixes
        CorrectionsHist->>GE2: Re-run validation
        GE2->>IcebergHist: Update quality statistics
    end
    
    IcebergHist->>PostgresHist: Integrate historical data
    
    Note over HistDAG: Historical processing complete
    
    Ops->>HistDAG: DEACTIVATE Historical DAG completely
    Ops->>LiveDAG: REACTIVATE Live DAG
    
    Note over LiveDAG: Process accumulated live files
```

## 5. Exclusive Mode Operation Rules

```mermaid
graph TB
    subgraph "Live Mode Active"
        LA1[Live DAG: ACTIVE]
        LA2[Historical DAG: INACTIVE]
        LA3[Live Files: PROCESSED immediately]
        LA4[Historical Files: NOT ACCESSIBLE]
        LA5[File Drop Location: MONITORED]
    end
    
    subgraph "Historical Mode Active"
        HA1[Live DAG: INACTIVE]
        HA2[Historical DAG: ACTIVE]
        HA3[Live Files: ACCUMULATE in drop folder]
        HA4[Historical Files: PROCESSED from archive]
        HA5[Historical Archive: MONITORED]
    end
    
    subgraph "Transition Rules"
        TR1[Manual Operations Control]
        TR2[Complete Deactivation Required]
        TR3[Never Concurrent Operation]
        TR4[Same 2 Spark Jobs Used]
    end
    
    TR1 --> LA1
    TR1 --> HA1
    TR2 --> LA2
    TR2 --> HA2
    TR3 --> TR1
    TR4 --> LA1
    TR4 --> HA1
```

## 6. Data Quality and Corrections Flow

```mermaid
graph TB
    subgraph "Quality Processing Steps"
        Q1[Raw Data Ingestion<br/>Live or Historical source]
        Q2[Spark Processing<br/>File reading and parsing]
        Q3[Great Expectations Initial<br/>Data validation and scoring]
        Q4[Iceberg Staging<br/>All data stored with quality flags]
        Q5{Quality Review}
        Q6[Clean Data Path<br/>Passes all validations]
        Q7[Problem Data Path<br/>Quality issues identified]
        Q8[Manual Corrections<br/>Applied to Iceberg staging]
        Q9[Great Expectations Re-run<br/>Validation on corrected data]
        Q10[PostgreSQL Load<br/>Only clean validated data]
    end
    
    Q1 --> Q2
    Q2 --> Q3
    Q3 --> Q4
    Q4 --> Q5
    Q5 -->|Clean| Q6
    Q5 -->|Issues| Q7
    Q7 --> Q8
    Q8 --> Q9
    Q9 --> Q6
    Q6 --> Q10
```

## System Operation Summary

### **Live Processing System Characteristics**
- **Data Source**: File drop location (real-time file arrivals)
- **Activation**: Default active mode during business hours
- **File Processing**: Immediate processing by universal priority
- **Quality Control**: Great Expectations validation → Iceberg staging → Manual corrections → PostgreSQL
- **Resource Usage**: Up to 2 Spark jobs available

### **Historical Processing System Characteristics**
- **Data Source**: Historical archive folder (configurable path parameter)
- **Activation**: Manual activation only (typically after-hours)
- **File Processing**: Batch processing by universal priority
- **Quality Control**: Same quality flow as live system
- **Resource Usage**: Same 2 Spark jobs when system is active

### **Exclusive Operation Rules**
1. **Single Active System**: Only Live OR Historical can be active, never both
2. **Complete Deactivation**: Inactive system is completely turned off
3. **File Accumulation**: Live files accumulate during historical processing
4. **Manual Control**: Operations team manually switches between modes
5. **Resource Sharing**: Same infrastructure used exclusively by active system

### **Universal Priority Logic** (Applied to Both Systems)
- **Primary**: Reference Period (YYYYMM)
- **Secondary**: Received Timestamp
- **Tertiary**: Provider Code (tie-breaker)
- **Result**: Chronological data processing regardless of file arrival order

### **Quality Assurance Process** (Both Systems)
1. **Initial Validation**: Great Expectations on raw data
2. **Staging**: All data loaded to Iceberg with quality flags
3. **Manual Review**: Corrections applied when quality issues found
4. **Re-validation**: Great Expectations re-run on corrected data
5. **Operational Load**: Only clean, validated data goes to PostgreSQL

---

**Data Flow Version**: 1.0 (Corrected and Independent)  
**Key Principle**: Two completely separate, exclusively operating systems  
**Quality Focus**: Staging-first with mandatory quality validation