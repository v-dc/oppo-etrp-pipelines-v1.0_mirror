import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook

# Read the original file
file_path = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/requirements_material/dictionary.xlsx'
output_dir = '/data1/projects/tvi/oppo-etrp-pipelines-v1.0/docs/dictionaries/'
output_path = os.path.join(output_dir, 'draft_dictionary.xlsx')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process fixed sheet
fixed_df = pd.read_excel(file_path, sheet_name='fixed')

# Define missing fields based on description analysis
fixed_field_mappings = {
    9: 'relationship_start_date',
    10: 'relationship_type',
    11: 'agreement_date',
    12: 'statement_date',
    13: 'capacity',
    14: 'facility',
    15: 'credit_limit',
    16: 'instalment_amount',
    17: 'amount_in_arrears',
    18: 'month_in_arrears',
    19: 'tenure',
    20: 'total_balance_outstanding',
    21: 'late_payment_interest',
    22: 'principal_repayment_term',
    23: 'collateral_type',
    24: 'legal_status',
    25: 'date_status_update',
    26: 'deletion_reason_code',
    27: 'total_amount_paid',
    28: 'debt_type',
    29: 'email',
    30: 'mobile_no',
    31: 'date_of_notice',
    32: 'sponsor_constitution',
    33: 'sponsor_old_ic_company_reg_no',
    34: 'sponsor_new_ic_business_reg_no',
    35: 'sponsor_passport_no',
    36: 'sponsor_name',
    37: 'sponsor_status',
    38: 'sponsor_remarks',
    39: 'old_account_no'
}

# Apply field mappings
for idx, field_name in fixed_field_mappings.items():
    fixed_df.loc[idx, 'field'] = field_name

# Define formats based on descriptions
fixed_format_mappings = {
    0: 'string(1)',  # payment_code
    1: 'string(1)',  # operation_code  
    2: 'string(1)',  # party_type
    3: 'string',     # name
    4: 'string',     # company_reg_no
    5: 'string',     # business_reg_no
    6: 'string',     # passport
    7: 'string',     # account
    8: 'integer',    # account_status
    9: 'date(yyyyMMdd)',   # relationship_start_date
    10: 'integer',   # relationship_type
    11: 'date(yyyyMMdd)',  # agreement_date
    12: 'date(yyyyMMdd)',  # statement_date
    13: 'integer',   # capacity
    14: 'integer',   # facility
    15: 'decimal',   # credit_limit
    16: 'decimal',   # instalment_amount
    17: 'decimal',   # amount_in_arrears
    18: 'integer',   # month_in_arrears
    19: 'integer',   # tenure
    20: 'decimal',   # total_balance_outstanding
    21: 'integer',   # late_payment_interest
    22: 'integer',   # principal_repayment_term
    23: 'integer',   # collateral_type
    24: 'integer',   # legal_status
    25: 'date(yyyyMMdd)',  # date_status_update
    26: 'integer',   # deletion_reason_code
    27: 'decimal',   # total_amount_paid
    28: 'string',    # debt_type
    29: 'email',     # email
    30: 'phone(601x-xxxxxxx)',  # mobile_no
    31: 'date(yyyyMMdd)',  # date_of_notice
    32: 'string(1)', # sponsor_constitution
    33: 'string',    # sponsor_old_ic_company_reg_no
    34: 'string',    # sponsor_new_ic_business_reg_no
    35: 'string',    # sponsor_passport_no
    36: 'string',    # sponsor_name
    37: 'integer',   # sponsor_status
    38: 'string',    # sponsor_remarks
    39: 'string'     # old_account_no
}

# Apply format mappings
for idx, format_val in fixed_format_mappings.items():
    fixed_df.loc[idx, 'format'] = format_val

# Define values based on descriptions
fixed_values_mappings = {
    0: '{"A", "M", "D"}',  # Already present
    1: '{"A", "M", "D"}',  # Already present
    2: '{"I", "C", "B"}',  # Fixed typo from "D" to "B"
    8: '{1, 2, 3, 4}',     # account_status
    10: '{1, 2, 3, 4, 5, 6, 7, 8}',  # relationship_type
    13: '{1, 2}',          # capacity
    14: '{1, 2, 3, 4, 5, 6}',  # facility
    22: '{1, 2, 3, 4, 5}', # principal_repayment_term
    23: '{0, 15}',         # collateral_type (from varying sheet example)
    24: '{1, 2}',          # legal_status
    26: '{1, 2, 3, 4, 5, 6, 7}',  # deletion_reason_code
    32: '{"I", "C", "B"}', # sponsor_constitution
    37: '{1, 2, 3}'        # sponsor_status
}

# Apply values mappings
for idx, values_val in fixed_values_mappings.items():
    fixed_df.loc[idx, 'values'] = values_val

# Process varying sheet
varying_df = pd.read_excel(file_path, sheet_name='varying')

# Define missing fields for varying sheet
varying_field_mappings = {
    2: 'relationship_start_date',
    3: 'relationship_type',
    4: 'statement_date',
    5: 'current',
    6: 'aging_30_days',
    7: 'aging_60_days',
    8: 'aging_90_days',
    9: 'aging_120_days',
    10: 'aging_150_days',
    11: 'aging_180_days',
    12: 'credit_limit',
    13: 'credit_term',
    14: 'collateral_type',
    15: 'deletion_reason_code',
    16: 'total_amount_paid',
    17: 'debt_type',
    18: 'home_address',
    19: 'home_city',
    20: 'home_state',
    21: 'home_zip_code',
    22: 'home_country',
    23: 'date_of_birth',
    24: 'nationality',
    25: 'email',
    26: 'home_tel',
    27: 'mobile_no',
    28: 'ref_no',
    29: 'date_of_notice',
    30: 'sponsor_constitution',
    31: 'sponsor_old_ic_company_reg_no',
    32: 'sponsor_new_ic_business_reg_no',
    33: 'sponsor_passport_no',
    34: 'sponsor_name',
    35: 'sponsor_status',
    36: 'sponsor_remarks',
    37: 'old_account_no',
    38: 'remark'
}

# Apply field mappings for varying
for idx, field_name in varying_field_mappings.items():
    varying_df.loc[idx, 'field'] = field_name

# Define formats for varying sheet
varying_format_mappings = {
    0: 'string',         # account
    1: 'integer',        # account_status
    2: 'date(yyyyMMdd)', # relationship_start_date
    3: 'integer',        # relationship_type
    4: 'date(yyyyMMdd)', # statement_date
    5: 'decimal',        # current
    6: 'decimal',        # aging_30_days
    7: 'decimal',        # aging_60_days
    8: 'decimal',        # aging_90_days
    9: 'decimal',        # aging_120_days
    10: 'decimal',       # aging_150_days
    11: 'decimal',       # aging_180_days
    12: 'decimal',       # credit_limit
    13: 'integer',       # credit_term
    14: 'integer',       # collateral_type
    15: 'integer',       # deletion_reason_code
    16: 'decimal',       # total_amount_paid
    17: 'integer',       # debt_type
    18: 'string',        # home_address
    19: 'string',        # home_city
    20: 'string',        # home_state
    21: 'string',        # home_zip_code
    22: 'string',        # home_country
    23: 'date(yyyyMMdd)',# date_of_birth
    24: 'string',        # nationality
    25: 'email',         # email
    26: 'phone(xxx-xxxxxxx)',   # home_tel
    27: 'phone(601x-xxxxxxx)',  # mobile_no
    28: 'string',        # ref_no
    29: 'date(yyyyMMdd)',# date_of_notice
    30: 'string(1)',     # sponsor_constitution
    31: 'string',        # sponsor_old_ic_company_reg_no
    32: 'string',        # sponsor_new_ic_business_reg_no
    33: 'string',        # sponsor_passport_no
    34: 'string',        # sponsor_name
    35: 'integer',       # sponsor_status
    36: 'string',        # sponsor_remarks
    37: 'string',        # old_account_no
    38: 'string'         # remark
}

# Apply format mappings for varying
for idx, format_val in varying_format_mappings.items():
    varying_df.loc[idx, 'format'] = format_val

# Define values for varying sheet
varying_values_mappings = {
    1: '{1, 2, 3, 4}',   # account_status
    3: '{1, 2, 3, 4, 5, 6, 7, 8}',  # relationship_type
    14: '{0, 15}',       # collateral_type
    15: '{1, 2, 3, 4, 5, 6}',  # deletion_reason_code
    30: '{"I", "C", "B"}',  # sponsor_constitution
    35: '{1, 2, 3}'      # sponsor_status
}

# Apply values mappings for varying
for idx, values_val in varying_values_mappings.items():
    varying_df.loc[idx, 'values'] = values_val

# Save to new Excel file
with pd.ExcelWriter(output_path) as writer:
    fixed_df.to_excel(writer, sheet_name='fixed', index=False)
    varying_df.to_excel(writer, sheet_name='varying', index=False)

print(f"Draft dictionary created successfully at: {output_path}")

# Summary of changes
print("\nSummary of populated fields:")
print(f"Fixed sheet: Added {len(fixed_field_mappings)} field names")
print(f"Fixed sheet: Added {len(fixed_format_mappings)} format values")
print(f"Fixed sheet: Added/corrected {len(fixed_values_mappings)} values entries")
print(f"Varying sheet: Added {len(varying_field_mappings)} field names")
print(f"Varying sheet: Added {len(varying_format_mappings)} format values")
print(f"Varying sheet: Added {len(varying_values_mappings)} values entries")