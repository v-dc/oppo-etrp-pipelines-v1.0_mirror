import pandas as pd

# Read the draft file
draft_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/dictionaries/draft_dictionary.xlsx'

# Check both sheets
for sheet_name in ['fixed', 'varying']:
    print(f"\n{'='*60}")
    print(f"Verifying {sheet_name} sheet")
    print('='*60)
    
    df = pd.read_excel(draft_path, sheet_name=sheet_name)
    
    # Count missing values
    missing_field = df['field'].isna().sum()
    missing_format = df['format'].isna().sum()
    missing_values = df['values'].isna().sum()
    
    print(f"Missing fields: {missing_field}")
    print(f"Missing formats: {missing_format}")
    print(f"Missing values: {missing_values}")
    
    # Show a sample of the populated data
    print(f"\nSample rows (first 3 with previously missing fields):")
    if sheet_name == 'fixed':
        sample_indices = [9, 10, 11]
    else:
        sample_indices = [2, 3, 4]
        
    for idx in sample_indices:
        row = df.iloc[idx]
        print(f"\nRow {idx}:")
        print(f"  Field: {row['field']}")
        print(f"  Format: {row['format']}")
        print(f"  Values: {row['values']}")
        print(f"  Description: {row['description'][:50]}...")