from pandas import read_csv
import os
from DataProcessor import *

def test_csv_import():
    dataproc = DataProcessor()
    datapath = r"Data_Files/Dataset1.csv"
    assert os.path.exists(datapath), f"FAILED locating CSV file in {datapath}"

    df = dataproc.importCSVdata(datapath)
    num_rows = len(df)
    num_cols = len(df.columns)

    assert num_rows == 201, f"FAILED data import. Number of rows: {num_rows}, Expected: {201}"
    assert num_cols == 2, f"FAILED data import. Number of columns: {num_cols}, Expected: {2}"