'''
<insert necessary documentation here>
'''

from pandas import read_csv
import os
from data_processor import DataProcessor

def test_csv_import():
    '''
    <insert necessary documentation here>
    '''
    dataproc = DataProcessor()
    datapath = r"Data_Files/Dataset1.csv"
    assert os.path.exists(datapath), f"FAILED locating CSV file in {datapath}"

    df = dataproc.import_csv_data(datapath)
    num_rows = len(df)
    num_cols = len(df.columns)

    assert num_rows == 201, f"FAILED data import. Number of rows: {num_rows}, Expected: {201}"
    assert num_cols == 2, f"FAILED data import. Number of columns: {num_cols}, Expected: {2}"