import pandas as pd
import random
import datetime
from faker import Faker
import os

# Initialize Faker with English locale (will generate Malaysian-style data manually)
fake = Faker('en_US')

# Define provider-specific loan types
PROVIDER_LOAN_TYPES = {
    'jcl': {
        'name': 'JCL Finance',
        'facilities': [1, 2],  # Trade Facilities, Goods & Services Receivables
        'typical_limits': (5000, 50000),
        'typical_tenure': (30, 180),
        'late_interest': (10, 18)
    },
    'boost': {
        'name': 'Boost Credit',
        'facilities': [2, 3],  # Goods & Services Receivables, Personal Financing
        'typical_limits': (1000, 20000),
        'typical_tenure': (7, 90),
        'late_interest': (12, 24)
    },
    'chinchin': {
        'name': 'ChinChin Capital',
        'facilities': [1, 4],  # Trade Facilities, Equipment/Vehicle Financing
        'typical_limits': (10000, 100000),
        'typical_tenure': (90, 365),
        'late_interest': (8, 15)
    }
}

def generate_malaysian_ic():
    """Generate Malaysian IC number"""
    year = random.randint(50, 99)
    month = f"{random.randint(1, 12):02d}"
    day = f"{random.randint(1, 28):02d}"
    state = random.choice(['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14'])
    numbers = f"{random.randint(1000, 9999):04d}"
    return f"{year}{month}{day}{state}{numbers}"

def generate_company_reg():
    """Generate Malaysian company registration number"""
    year = random.randint(2000, 2024)
    numbers = f"{random.randint(100000, 999999):06d}"
    suffix = random.choice(['M', 'H', 'X', 'W', 'K'])
    return f"{year}{numbers}-{suffix}"

def generate_mobile():
    """Generate Malaysian mobile number"""
    prefix = random.choice(['012', '013', '014', '016', '017', '018', '019'])
    number = f"{random.randint(1000000, 9999999):07d}"
    return f"{prefix}-{number}"

def generate_sample_data(provider_key, num_rows=1000):
    """Generate sample data for a specific provider"""
    provider = PROVIDER_LOAN_TYPES[provider_key]
    data = []
    
    # Get field information from dictionary
    dict_df = pd.read_excel('docs/dictionaries/draft_dictionary.xlsx')
    fields = dict_df['field'].tolist()
    
    for i in range(num_rows):
        row = {}
        
        # Basic fields
        row['payment_code'] = 'A' if i < num_rows * 0.8 else random.choice(['M', 'D'])
        row['operation_code'] = random.choice(['A', 'M', 'D']) if row['payment_code'] != 'A' else 'A'
        
        # Party type distribution: 70% individual, 20% company, 10% both
        row['party_type'] = random.choices(['I', 'C', 'B'], weights=[70, 20, 10])[0]
        
        # Name based on party type
        if row['party_type'] == 'I':
            row['name'] = fake.name().upper()
            row['company_reg_no'] = ''
            row['business_reg_no'] = generate_malaysian_ic()
        elif row['party_type'] == 'C':
            row['name'] = fake.company().upper() + ' SDN BHD'
            row['company_reg_no'] = generate_company_reg()
            row['business_reg_no'] = row['company_reg_no']
        else:  # Both
            row['name'] = fake.name().upper() + ' & ' + fake.company().upper()
            row['company_reg_no'] = generate_company_reg()
            row['business_reg_no'] = generate_malaysian_ic()
        
        row['passport'] = '' if random.random() > 0.05 else fake.lexify('?#######').upper()
        row['account'] = f"{provider_key.upper()}{i+1:06d}"
        
        # Account status: 80% active, 10% closed, 5% dormant, 5% bad debt
        row['account_status'] = random.choices([1, 2, 3, 4], weights=[80, 10, 5, 5])[0]
        
        # Dates
        start_date = fake.date_between(start_date='-3y', end_date='-1m')
        row['relationship_start_date'] = start_date.strftime('%Y%m%d')
        row['relationship_type'] = 1  # Customer
        
        agreement_date = start_date + datetime.timedelta(days=random.randint(0, 30))
        row['agreement_date'] = agreement_date.strftime('%Y%m%d')
        
        # Ensure statement date is after agreement date and not in the future
        today = datetime.date.today()
        if agreement_date < today:
            statement_date = fake.date_between(start_date=agreement_date, end_date='today')
        else:
            statement_date = agreement_date
        row['statement_date'] = statement_date.strftime('%Y%m%d')
        
        row['capacity'] = random.choices([1, 2], weights=[85, 15])[0]
        row['facility'] = random.choice(provider['facilities'])
        
        # Financial details
        row['credit_limit'] = round(random.uniform(*provider['typical_limits']), 2)
        row['tenure'] = random.randint(*provider['typical_tenure'])
        
        # Calculate installment based on credit limit and tenure
        row['instalment_amount'] = round(row['credit_limit'] / (row['tenure'] / 30), 2)
        
        # Balance and arrears
        if row['account_status'] == 1:  # Active
            row['total_balance_outstanding'] = round(random.uniform(0, row['credit_limit']), 2)
            if random.random() < 0.3:  # 30% have arrears
                row['month_in_arrears'] = random.randint(1, 6)
                row['amount_in_arrears'] = round(row['instalment_amount'] * row['month_in_arrears'], 2)
            else:
                row['month_in_arrears'] = 0
                row['amount_in_arrears'] = 0.00
        else:
            row['total_balance_outstanding'] = 0.00 if row['account_status'] == 2 else round(random.uniform(0, row['credit_limit']), 2)
            row['month_in_arrears'] = 0 if row['account_status'] == 2 else random.randint(3, 12)
            row['amount_in_arrears'] = 0.00 if row['account_status'] == 2 else round(row['instalment_amount'] * row['month_in_arrears'], 2)
        
        row['late_payment_interest'] = random.randint(*provider['late_interest'])
        row['principal_repayment_term'] = 1  # Monthly
        
        # Collateral and legal status
        row['collateral_type'] = random.randint(1, 5) if row['facility'] in [1, 4] else 0
        row['legal_status'] = 0
        if row['month_in_arrears'] > 3:
            row['legal_status'] = random.choices([0, 1, 2], weights=[50, 30, 20])[0]
        
        row['date_status_update'] = statement_date.strftime('%Y%m%d')
        
        # Deletion reason (only for D operation)
        row['deletion_reason_code'] = random.randint(1, 3) if row['operation_code'] == 'D' else 0
        row['total_amount_paid'] = row['credit_limit'] if row['deletion_reason_code'] == 1 else 0.00
        
        row['debt_type'] = random.choice(['001', '002', '003', '004'])
        
        # Contact info (70% have email, 80% have mobile)
        row['email'] = fake.email() if random.random() < 0.7 else ''
        row['mobile_no'] = generate_mobile() if random.random() < 0.8 else ''
        
        # Notice date for accounts with legal status
        if row['legal_status'] > 0:
            notice_date = statement_date - datetime.timedelta(days=random.randint(30, 90))
            row['date_of_notice'] = notice_date.strftime('%Y%m%d')
        else:
            row['date_of_notice'] = ''
        
        # Sponsor information (20% of accounts)
        if random.random() < 0.2:
            row['sponsor_constitution'] = random.choice(['I', 'C'])
            if row['sponsor_constitution'] == 'I':
                row['sponsor_old_ic_company_reg_no'] = ''
                row['sponsor_new_ic_business_reg_no'] = generate_malaysian_ic()
                row['sponsor_name'] = fake.name().upper()
            else:
                reg_no = generate_company_reg()
                row['sponsor_old_ic_company_reg_no'] = reg_no
                row['sponsor_new_ic_business_reg_no'] = reg_no
                row['sponsor_name'] = fake.company().upper() + ' SDN BHD'
            row['sponsor_passport_no'] = ''
            row['sponsor_status'] = 1
            row['sponsor_remarks'] = random.choice(['GUARANTOR', 'CO-BORROWER', ''])
        else:
            row['sponsor_constitution'] = ''
            row['sponsor_old_ic_company_reg_no'] = ''
            row['sponsor_new_ic_business_reg_no'] = ''
            row['sponsor_passport_no'] = ''
            row['sponsor_name'] = ''
            row['sponsor_status'] = ''
            row['sponsor_remarks'] = ''
        
        row['old_account_no'] = ''
        
        data.append(row)
    
    # Create DataFrame with all fields in order
    df = pd.DataFrame(data)
    ordered_df = pd.DataFrame()
    for field in fields:
        if field in df.columns:
            ordered_df[field] = df[field]
        else:
            ordered_df[field] = ''
    
    return ordered_df

def main():
    """Generate sample files for all providers"""
    # Create samples directory if it doesn't exist
    os.makedirs('samples', exist_ok=True)
    
    # File specifications
    files_to_generate = [
        ('jcl', '202412', '20250104', '0925'),
        ('boost', '202411', '20241229', '1715'),
        ('chinchin', '202412', '20250117', '1407')
    ]
    
    for provider, ref_period, rec_date, rec_time in files_to_generate:
        filename = f"{provider}_{ref_period}_{rec_date}_{rec_time}.txt"
        filepath = os.path.join('samples', filename)
        
        print(f"Generating {filename}...")
        df = generate_sample_data(provider, 1000)
        
        # Save as pipe-delimited file
        df.to_csv(filepath, sep='|', index=False)
        print(f"Generated {filename} with {len(df)} rows")

if __name__ == "__main__":
    main()