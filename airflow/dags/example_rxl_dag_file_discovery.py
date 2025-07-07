import yaml
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from airflow_paths import AIRFLOW_CONFIG_PATH

try:
    with open(AIRFLOW_CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
except yaml.YAMLError as e:
    raise (f'Error reading YAML file: {e}')

VENV_PATH = config['package']['venv']
PACKAGE_ROOT = config['package']['root']


def extract_info_from_filename(filename: str):
    """
    Extracts information from the filename.
    Args:
        filename (str): The name of the file.
    Returns:
        dict: A dictionary containing the extracted information.
    """
    import os
    from datetime import datetime

    #  <provider-code>_<ref-period>_<received-time-stamp>
    #  e.g: MG00047_202403_20240401_1339_16.txt
    root, _ = os.path.splitext(filename)
    info = root.split('_')
    provider_code = info[0]
    ref_int = int(info[1])
    rec_int = int(f'{info[2]}{info[3]}{info[4]}')
    ref_month = datetime.strptime(info[1], '%Y%m').date()
    ref_year = datetime.strptime(str(ref_int // 100), '%Y').date()
    rec_timestamp = datetime.strptime(f'{info[2]}{info[3]}{info[4]}', '%Y%m%d%H%M%S')
    rec_year = datetime.strptime(str(rec_int // 10_000_000_000), '%Y').date()
    rec_month = datetime.strptime(str(rec_int // 100_000_000), '%Y%m').date()
    rec_day = datetime.strptime(str(rec_int // 1_000_000), '%Y%m%d').date()
    # ref_month = int(info[1])
    # ref_year = ref_month // 100
    # rec_timestamp = int(f'{info[2]}{info[3]}{info[4]}')
    # rec_year = rec_timestamp // 10_000_000_000
    # rec_month = rec_timestamp // 100_000_000
    # rec_day = rec_timestamp // 1_000_000

    return {
        'filename': filename, 
        'provider_code': provider_code, 
        'ref_year': ref_year,
        'ref_month': ref_month, 
        'rec_timestamp': rec_timestamp,
        'rec_year': rec_year,
        'rec_month': rec_month,
        'rec_day': rec_day
    }


with DAG(
    dag_id='file_discovery',
    description='A DAG for raw file discovery',
    schedule=None,
    max_active_runs=1,
    params={
        'source_directory': Param(
            default='/data1/systems/cb-system/data/raw_bak',
            type='string',
            description='The source directory for ingesting new files',
        ),
        'pattern': Param(
            default='[A-Z][A-Z][0-9]*_[0-9]*_[0-9]*_[0-9]*_[0-9]*.txt',
            type='string',
            description='Glob pattern for matching files in the source directory',
        ),
    },
    tags=['iceberg']
) as dag:

    @task
    def get_list_files(params: dict):
        import os
        import glob

        source_directory = params['source_directory']
        pattern = params['pattern']

        file_pattern = os.path.join(source_directory, pattern)
        matched_files = glob.glob(file_pattern)
        # Extract just the filenames, not full paths
        files = [os.path.basename(f) for f in matched_files]

        return files

    @task
    def update_file_table(files: list[str], params: dict):
        """
        Extract metadata from the incoming files and upload the information to the table in the warehouse.
        """
        # import os
        import sys
        # import subprocess
        import pandas as pd

        sys.path.append(PACKAGE_ROOT)
        from src.utils.spark import get_spark_session

        data = []

        for filename in files:
            extract_info = extract_info_from_filename(filename)
            provider_code = extract_info['provider_code']
            ref_month = extract_info['ref_month']
            ref_year = extract_info['ref_year']
            rec_year = extract_info['rec_year']
            rec_month = extract_info['rec_month']
            rec_day = extract_info['rec_day']
            rec_timestamp = extract_info['rec_timestamp']

            data.append({
                'source_directory': params['source_directory'],
                'filename': filename, 
                'provider_code': provider_code,
                'ref_month': ref_month,
                'ref_year': ref_year,
                'rec_year': rec_year,
                'rec_month': rec_month,
                'rec_day': rec_day,
                'rec_timestamp': rec_timestamp
            })

        files_found_df = pd.DataFrame(data)

        spark = get_spark_session()

        files_found_df = spark.createDataFrame(files_found_df)
        table_exists = spark.catalog.tableExists('jdbc_prod.default.file_discovery')
        if table_exists:
            # If the table exists, drop the table
            spark.sql('drop table if exists jdbc_prod.default.file_discovery purge')
        
        # Create file_discovery table
        files_found_df.writeTo('jdbc_prod.default.file_discovery').using('iceberg').create()

        spark.stop()

        return files
    
    @task
    def file_discovery_report():
        """
        Create a simple report that prints the file discovery table.
        """
        import os
        import sys
        import pandas as pd
        from datetime import datetime

        sys.path.append(PACKAGE_ROOT)
        from src.utils.spark import get_spark_session
        from src.utils.paths import STORAGE_PATH

        spark = get_spark_session()

        # Read the file_discovery table
        df = spark.read.table('jdbc_prod.default.file_discovery')

        # Convert to Pandas DataFrame for easier manipulation
        pdf = df.toPandas()

        # Write the DataFrame to an Excel file using xlsxwriter
        output_dir = os.path.join(STORAGE_PATH, 'file_discovery')
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory
        excel_path = os.path.join(output_dir, f'file_discovery_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')

        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            pdf.to_excel(writer, index=False, sheet_name='FileDiscovery')

        spark.stop()


    ### Workflow ###

    # Create the file list once
    file_list_1 = get_list_files()

    # Update the file table with the list of files
    file_list_2 = update_file_table(files=file_list_1)

    # Create a report of the file discovery table
    file_discovery_report_task = file_discovery_report()

    # Set dependencies
    file_list_1 >> file_list_2 >> file_discovery_report_task