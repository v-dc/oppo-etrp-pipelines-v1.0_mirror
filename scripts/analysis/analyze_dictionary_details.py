import pandas as pd
import numpy as np

# Read the Excel file
file_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/requirements_material/dictionary.xlsx'

# Process each sheet
for sheet_name in ['fixed', 'varying']:
    print(f"\n{'='*80}")
    print(f"Analyzing Sheet: {sheet_name}")
    print('='*80)
    
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Show rows with missing fields
    print("\nRows with missing 'field' values:")
    missing_field = df[df['field'].isna()]
    for idx, row in missing_field.iterrows():
        print(f"\nRow {idx}:")
        print(f"  Description: {row['description']}")
        print(f"  Example 1: {row['example_1']}")
        print(f"  Example 2: {row['example_2']}")
        print(f"  Example 3: {row['example_3']}")
        print(f"  Example 4: {row['example_4']}")
        print(f"  Format: {row['format']}")
        print(f"  Values: {row['values']}")
    
    # Show rows with missing format
    print("\n\nRows with missing 'format' values:")
    missing_format = df[df['format'].isna()]
    for idx, row in missing_format.iterrows():
        if pd.notna(row['field']):  # Only show if field is not also missing
            print(f"\nRow {idx} - Field: {row['field']}")
            print(f"  Description: {row['description']}")
            print(f"  Values: {row['values']}")
            print(f"  Example 1: {row['example_1']}")
    
    # Show rows with missing values
    print("\n\nRows with missing 'values' column:")
    missing_values = df[df['values'].isna()]
    for idx, row in missing_values.iterrows():
        if pd.notna(row['field']):  # Only show if field is not also missing
            print(f"\nRow {idx} - Field: {row['field']}")
            print(f"  Description: {row['description']}")
            print(f"  Example 1: {row['example_1']}")
            print(f"  Example 2: {row['example_2']}")
            
    # Summary
    print(f"\n\nSummary for {sheet_name} sheet:")
    print(f"  Total rows: {len(df)}")
    print(f"  Rows with missing field: {len(missing_field)}")
    print(f"  Rows with missing format: {len(missing_format)}")
    print(f"  Rows with missing values: {len(missing_values)}")