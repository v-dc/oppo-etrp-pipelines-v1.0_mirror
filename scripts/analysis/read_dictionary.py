import pandas as pd
import openpyxl

# Read the Excel file
file_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/requirements_material/dictionary.xlsx'
xl_file = pd.ExcelFile(file_path)

# List all sheet names
print("Sheets in the file:")
for sheet in xl_file.sheet_names:
    print(f"  - {sheet}")

# Read each sheet
for sheet_name in xl_file.sheet_names:
    print(f"\n{'='*60}")
    print(f"Sheet: {sheet_name}")
    print('='*60)
    
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Display columns
    print(f"\nColumns: {list(df.columns)}")
    print(f"Number of rows: {len(df)}")
    
    # Display first few rows to understand the structure
    print(f"\nFirst 5 rows:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    print(df.head())