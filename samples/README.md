# CB-Core Samples Directory

## Overview
Sample data files and examples for CB-Core development and testing.

## Files

### Credit Bureau Sample Data
- **OT00005_202412_20250116_0946_25.txt**: Real credit bureau file sample
  - Institution: OT00005 (Other institution type)
  - Period: 202412 (December 2024)
  - Received: 20250116_0946 (January 16, 2025 at 09:46)
  - Sequence: 25
  - Format: 63-field pipe-delimited
  - Use: Development, testing, schema validation

### File Format
- **Delimiter**: Pipe (|)
- **Fields**: 63 fields per record
- **Structure**: Origination data (fields 1-31) + Servicing data (fields 32-63)
- **Encoding**: UTF-8 text

## Usage

### For Development
```python
# Read sample file
sample_file = "samples/OT00005_202412_20250116_0946_25.txt"
df = spark.read.option("delimiter", "|").csv(sample_file)
```

### For Testing
```python
# Use in test fixtures
@pytest.fixture
def sample_credit_file():
    return "samples/OT00005_202412_20250116_0946_25.txt"
```

### For Schema Validation
- Use to test data quality rules
- Validate field definitions
- Test transformation logic

## Reference Files
For complete metadata, see:
- `/data1/systems/cb-system/data/raw-dictionary/dictionary_fields_final.csv`
- `/data1/systems/cb-system/data/raw-dictionary/institution_final.csv`

Note: Reference files are read-only and located outside the cb-core repository.
