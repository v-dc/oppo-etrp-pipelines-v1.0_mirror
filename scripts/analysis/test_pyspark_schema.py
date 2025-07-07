#!/usr/bin/env python3
"""
Test script to read sample files using PySpark with the draft_schema_raw schema
"""
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType
from pyspark.sql.functions import col, count, when, isnan, isnull
import yaml

def create_spark_session():
    """Create and return a Spark session"""
    spark = SparkSession.builder \
        .appName("Test Draft Schema Raw") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def load_schema_from_yaml(yaml_path):
    """Load schema definition from YAML file"""
    with open(yaml_path, 'r') as f:
        schema_def = yaml.safe_load(f)
    return schema_def

def create_pyspark_schema():
    """Create PySpark schema based on draft_schema_raw.yaml"""
    # Define the schema as per the YAML file
    draft_schema_raw = StructType([
        StructField("payment_code", StringType(), False),
        StructField("operation_code", StringType(), False),
        StructField("party_type", StringType(), False),
        StructField("name", StringType(), False),
        StructField("company_reg_no", StringType(), True),
        StructField("business_reg_no", StringType(), True),
        StructField("passport", StringType(), True),
        StructField("account", StringType(), False),
        StructField("account_status", IntegerType(), False),
        StructField("relationship_start_date", StringType(), False),
        StructField("relationship_type", IntegerType(), False),
        StructField("agreement_date", StringType(), False),
        StructField("statement_date", StringType(), True),
        StructField("capacity", IntegerType(), True),
        StructField("facility", IntegerType(), True),
        StructField("credit_limit", DecimalType(18, 2), True),
        StructField("instalment_amount", DecimalType(18, 2), True),
        StructField("amount_in_arrears", DecimalType(18, 2), True),
        StructField("month_in_arrears", IntegerType(), True),
        StructField("tenure", IntegerType(), True),
        StructField("total_balance_outstanding", DecimalType(18, 2), True),
        StructField("late_payment_interest", IntegerType(), True),
        StructField("principal_repayment_term", IntegerType(), True),
        StructField("collateral_type", IntegerType(), True),
        StructField("legal_status", IntegerType(), True),
        StructField("date_status_update", StringType(), True),
        StructField("deletion_reason_code", IntegerType(), True),
        StructField("total_amount_paid", DecimalType(18, 2), True),
        StructField("debt_type", StringType(), True),
        StructField("email", StringType(), True),
        StructField("mobile_no", StringType(), True),
        StructField("date_of_notice", StringType(), True),
        StructField("sponsor_constitution", StringType(), True),
        StructField("sponsor_old_ic_company_reg_no", StringType(), True),
        StructField("sponsor_new_ic_business_reg_no", StringType(), True),
        StructField("sponsor_passport_no", StringType(), True),
        StructField("sponsor_name", StringType(), True),
        StructField("sponsor_status", IntegerType(), True),
        StructField("sponsor_remarks", StringType(), True),
        StructField("old_account_no", StringType(), True)
    ])
    return draft_schema_raw

def analyze_dataframe(df, file_name):
    """Analyze the loaded DataFrame and print statistics"""
    print(f"\n{'='*60}")
    print(f"Analysis of {file_name}")
    print(f"{'='*60}")
    
    # Basic info
    print(f"\nTotal rows: {df.count()}")
    print(f"Total columns: {len(df.columns)}")
    
    # Check for any parsing errors
    print("\n--- Data Quality Checks ---")
    
    # Check account status distribution
    print("\nAccount Status Distribution:")
    df.groupBy("account_status").count().orderBy("account_status").show()
    
    # Check party type distribution
    print("\nParty Type Distribution:")
    df.groupBy("party_type").count().orderBy("party_type").show()
    
    # Check operation code distribution
    print("\nOperation Code Distribution:")
    df.groupBy("operation_code").count().orderBy("operation_code").show()
    
    # Check for null values in mandatory fields
    mandatory_fields = ["payment_code", "operation_code", "party_type", "name", 
                       "account", "account_status", "relationship_start_date", 
                       "relationship_type", "agreement_date"]
    
    print("\nNull check for mandatory fields:")
    for field in mandatory_fields:
        null_count = df.filter(col(field).isNull()).count()
        if null_count > 0:
            print(f"  {field}: {null_count} nulls found!")
        else:
            print(f"  {field}: OK (no nulls)")
    
    # Financial statistics
    print("\nFinancial Statistics:")
    df.select(
        "credit_limit", 
        "instalment_amount", 
        "amount_in_arrears", 
        "total_balance_outstanding"
    ).summary().show()
    
    # Sample data
    print("\nSample records (first 5):")
    df.select(
        "account", "name", "party_type", "account_status", 
        "credit_limit", "total_balance_outstanding"
    ).show(5, truncate=False)

def main():
    """Main function to test reading sample files with PySpark schema"""
    # Initialize Spark
    print("Initializing Spark session...")
    spark = create_spark_session()
    
    try:
        # Load schema
        print("Loading PySpark schema...")
        schema = create_pyspark_schema()
        
        # Define sample file to test
        sample_file = "samples/jcl_202412_20250104_0925.txt"
        
        if not os.path.exists(sample_file):
            print(f"Error: Sample file {sample_file} not found!")
            return
        
        print(f"\nReading file: {sample_file}")
        
        # Read the file with schema
        df = spark.read \
            .option("header", "true") \
            .option("delimiter", "|") \
            .option("mode", "PERMISSIVE") \
            .option("columnNameOfCorruptRecord", "_corrupt_record") \
            .schema(schema) \
            .csv(sample_file)
        
        # Cache the DataFrame for better performance
        df.cache()
        
        # Analyze the data
        analyze_dataframe(df, sample_file)
        
        # Check for any corrupt records
        if "_corrupt_record" in df.columns:
            corrupt_count = df.filter(col("_corrupt_record").isNotNull()).count()
            if corrupt_count > 0:
                print(f"\nWARNING: Found {corrupt_count} corrupt records!")
                print("Sample corrupt records:")
                df.filter(col("_corrupt_record").isNotNull()).show(5, truncate=False)
        
        # Test reading other sample files
        other_files = [
            "samples/boost_202411_20241229_1715.txt",
            "samples/chinchin_202412_20250117_1407.txt"
        ]
        
        print("\n" + "="*60)
        print("Quick validation of other sample files:")
        print("="*60)
        
        for file in other_files:
            if os.path.exists(file):
                df_test = spark.read \
                    .option("header", "true") \
                    .option("delimiter", "|") \
                    .schema(schema) \
                    .csv(file)
                print(f"\n{file}: {df_test.count()} rows loaded successfully")
            else:
                print(f"\n{file}: File not found")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop Spark session
        print("\nStopping Spark session...")
        spark.stop()

if __name__ == "__main__":
    main()