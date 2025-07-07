# Analysis Scripts Documentation

This directory contains Python scripts for analyzing, processing, and validating data dictionaries and generating sample data files for the OPPO eTRP pipelines project.

## Scripts Overview

### 1. `analyze_dictionary_details.py`
**Purpose**: Analyzes the original dictionary Excel file to identify data quality issues.
- Reads `dictionary.xlsx` from the requirements_material folder
- Processes both 'fixed' and 'varying' sheets
- Identifies rows with missing field names, format specifications, and values
- Helps identify incomplete or problematic entries that need attention

**Usage**: `python analyze_dictionary_details.py`

---

### 2. `check_doubtful_rows.py`
**Purpose**: Examines specific problematic rows in the dictionary that need clarification.
- Focuses on rows with questionable or unclear data
- Checks issues in both fixed and varying sheets:
  - Statement Date format consistency
  - Debt Type missing descriptions
  - Collateral Type valid codes
- Outputs detailed information for manual review

**Usage**: `python check_doubtful_rows.py`

---

### 3. `create_draft_dictionary.py`
**Purpose**: Creates a draft version of the dictionary with missing fields populated.
- Reads the original `dictionary.xlsx` file
- Creates `draft_dictionary.xlsx` in the dictionaries folder
- Maps descriptive entries to appropriate field names
- Populates missing field names like:
  - relationship_start_date
  - credit_limit
  - collateral_type
  - debt_type

**Usage**: `python create_draft_dictionary.py`

---

### 4. `generate_sample_files.py`
**Purpose**: Generates realistic sample data files based on the draft dictionary schema.
- Creates pipe-delimited text files with Malaysian data
- Generates 1000 rows per file
- Creates files for three providers: JCL, Boost, and ChinChin
- Follows naming convention: `{provider}_{reference_period}_{received_date}_{received_time}.txt`
- Uses Faker library to generate realistic names, addresses, and IDs
- Implements provider-specific loan characteristics

**Usage**: `python generate_sample_files.py`

**Output**: Creates files in the `samples/` directory

---

### 5. `read_dictionary.py`
**Purpose**: Simple reader script to explore the structure of dictionary Excel files.
- Lists all sheet names in the Excel file
- Displays columns and row counts for each sheet
- Shows first 5 rows of each sheet
- Useful for understanding file structure

**Usage**: `python read_dictionary.py`

---

### 6. `test_pyspark_schema.py`
**Purpose**: Tests reading sample data files using PySpark with the defined schema.
- Loads the PySpark schema from `schemas/draft_schema_raw.yaml`
- Reads pipe-delimited sample files
- Validates data quality:
  - Checks for null values in mandatory fields
  - Analyzes account status distribution
  - Generates financial statistics
- Tests all sample files for compatibility

**Usage**: `python test_pyspark_schema.py`

**Requirements**: PySpark 3.5.x, PyYAML

---

### 7. `update_draft_dictionary.py`
**Purpose**: Updates the draft dictionary based on specific clarifications.
- Applies targeted updates to `draft_dictionary.xlsx`
- Updates field formats and values based on requirements:
  - Debt Type format to 'char(3)'
  - Collateral Type values to {0, 15}
  - Date formats to 'date(yyyyMMdd)'
- Saves updates back to the same file

**Usage**: `python update_draft_dictionary.py`

---

### 8. `verify_draft.py`
**Purpose**: Validates the completeness of the draft dictionary after updates.
- Reads `draft_dictionary.xlsx`
- Counts missing fields, formats, and values
- Displays sample rows that were previously incomplete
- Ensures the dictionary is ready for use

**Usage**: `python verify_draft.py`

---

## Workflow

The typical workflow for using these scripts:

1. **Analyze** - Run `analyze_dictionary_details.py` to identify issues in the original dictionary
2. **Review** - Use `check_doubtful_rows.py` to examine specific problematic entries
3. **Create** - Execute `create_draft_dictionary.py` to generate a draft with populated fields
4. **Update** - Run `update_draft_dictionary.py` to apply clarifications and fixes
5. **Verify** - Use `verify_draft.py` to validate the final dictionary
6. **Generate** - Run `generate_sample_files.py` to create test data files
7. **Test** - Execute `test_pyspark_schema.py` to validate data loading with PySpark

## Dependencies

- pandas
- openpyxl
- faker (for generate_sample_files.py)
- pyspark==3.5.x (for test_pyspark_schema.py)
- pyyaml (for test_pyspark_schema.py)

## Notes

- All scripts assume the virtual environment is activated: `source .venv/bin/activate`
- Input files are expected in `docs/requirements_material/` or `docs/dictionaries/`
- Output files are created in `docs/dictionaries/` or `samples/`
- The schema definition is stored in `schemas/draft_schema_raw.yaml`