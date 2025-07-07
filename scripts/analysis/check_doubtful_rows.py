import pandas as pd

# Read the original file to check specific doubtful rows
file_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/requirements_material/dictionary.xlsx'

print("DOUBTFUL ROWS TO CLARIFY:\n")

# Fixed sheet doubts
print("FIXED SHEET:")
print("="*60)

fixed_df = pd.read_excel(file_path, sheet_name='fixed')

# 1. Row 4 - Statement Date
print("\n1. Row 4 (index 12) - Statement Date:")
print(f"   Description: {fixed_df.iloc[12]['description']}")
print(f"   Examples: {fixed_df.iloc[12]['example_1']}, {fixed_df.iloc[12]['example_2']}, {fixed_df.iloc[12]['example_3']}, {fixed_df.iloc[12]['example_4']}")
print("   DOUBT: Examples show proper dates (20230228, etc.) but format is yyyyMMdd - looks correct")

# 2. Row 28 - Debt Type
print("\n2. Row 28 - Debt Type:")
print(f"   Description: {fixed_df.iloc[28]['description']}")
print(f"   Examples: {fixed_df.iloc[28]['example_1']}, {fixed_df.iloc[28]['example_2']}, {fixed_df.iloc[28]['example_3']}, {fixed_df.iloc[28]['example_4']}")
print("   DOUBT: No description or examples provided. What are the valid debt types?")

# 3. Row 23 - Collateral Type
print("\n3. Row 23 - Collateral Type:")
print(f"   Description: {fixed_df.iloc[23]['description']}")
print(f"   Examples: {fixed_df.iloc[23]['example_1']}, {fixed_df.iloc[23]['example_2']}, {fixed_df.iloc[23]['example_3']}, {fixed_df.iloc[23]['example_4']}")
print("   DOUBT: All examples show '0', but varying sheet shows '15' as deposit. Are there other codes?")

# Varying sheet doubts
print("\n\nVARYING SHEET:")
print("="*60)

varying_df = pd.read_excel(file_path, sheet_name='varying')

# 4. Row 4 - Statement Date in varying
print("\n4. Row 4 (index 4) - Statement Date:")
print(f"   Description: {varying_df.iloc[4]['description']}")
print(f"   Examples: {varying_df.iloc[4]['example_1']}, {varying_df.iloc[4]['example_2']}, {varying_df.iloc[4]['example_3']}, {varying_df.iloc[4]['example_4']}")
print("   DOUBT: Examples show '43739' which doesn't match yyyyMMdd format. Is this Excel serial date?")

# 5. Row 17 - Debt Type in varying
print("\n5. Row 17 - Debt Type:")
print(f"   Description: {varying_df.iloc[17]['description']}")
print(f"   Examples: {varying_df.iloc[17]['example_1']}, {varying_df.iloc[17]['example_2']}, {varying_df.iloc[17]['example_3']}, {varying_df.iloc[17]['example_4']}")
print("   DOUBT: Examples show 1, 2, 3, 4 but no description of what these codes mean")

# 6. Row 29 - Date of Notice
print("\n6. Row 29 - Date of Notice:")
print(f"   Description: {varying_df.iloc[29]['description']}")
print(f"   Examples: {varying_df.iloc[29]['example_1']}, {varying_df.iloc[29]['example_2']}, {varying_df.iloc[29]['example_3']}, {varying_df.iloc[29]['example_4']}")
print("   DOUBT: Examples show '43739' but description says yyyyMMdd format. Same issue as statement date")

# 7. Credit Term units
print("\n7. Row 13 (varying) - Credit Term:")
print(f"   Description: {varying_df.iloc[13]['description']}")
print(f"   Examples: {varying_df.iloc[13]['example_1']}, {varying_df.iloc[13]['example_2']}, {varying_df.iloc[13]['example_3']}, {varying_df.iloc[13]['example_4']}")
print("   DOUBT: Description says 'how many days' and examples show 30, so assuming days as unit")

# 8. Deletion Reason Code difference
print("\n8. Deletion Reason Code - Different between sheets:")
print("   Fixed sheet: Has code 7 (Refund)")
print("   Varying sheet: Does NOT have code 7")
print("   DOUBT: Should both sheets have the same deletion reason codes?")