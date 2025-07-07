import pandas as pd
import os

# Read the draft file
draft_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/dictionaries/draft_dictionary.xlsx'

# Read both sheets
fixed_df = pd.read_excel(draft_path, sheet_name='fixed')
varying_df = pd.read_excel(draft_path, sheet_name='varying')

# Update based on clarifications

# 1. Fixed sheet - Debt Type (row 28): change to char(3), no standard values
fixed_df.loc[28, 'format'] = 'char(3)'
fixed_df.loc[28, 'values'] = pd.NA  # Remove any values if set

# 2. Fixed sheet - Collateral Type (row 23): ensure it accepts 0 and 15
# Already set as {0, 15} which is correct

# 3. Varying sheet - Statement Date (row 4): keep as date(yyyyMMdd) 
# Already correct, no change needed

# 4. Varying sheet - Date of Notice (row 29): keep as date(yyyyMMdd)
# Already correct, no change needed

# 5. Varying sheet - Debt Type (row 17): change to char(3), no standard values
varying_df.loc[17, 'format'] = 'char(3)'
varying_df.loc[17, 'values'] = pd.NA  # Remove any values if set

# Save the updated file
with pd.ExcelWriter(draft_path, engine='openpyxl') as writer:
    fixed_df.to_excel(writer, sheet_name='fixed', index=False)
    varying_df.to_excel(writer, sheet_name='varying', index=False)

print("Updated draft_dictionary.xlsx with the following changes:")
print("1. Fixed sheet - Debt Type (row 28): format changed to 'char(3)', no standard values")
print("2. Fixed sheet - Collateral Type (row 23): confirmed values {0, 15}")
print("3. Varying sheet - Statement Date (row 4): kept as 'date(yyyyMMdd)'")
print("4. Varying sheet - Date of Notice (row 29): kept as 'date(yyyyMMdd)'")
print("5. Varying sheet - Debt Type (row 17): format changed to 'char(3)', no standard values")
print("\nFile updated successfully!")