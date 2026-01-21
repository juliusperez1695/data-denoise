'''
<insert necessary documentation here>
'''

import os
import pandas as pd
from data_processor import DataProcessor

def test_parabola_outliers1():
    '''
    <insert necessary documentation here>
    '''
    datapath = r"Data_Files/parabola1.csv"
    assert os.path.exists(datapath), f"FAILED to locate file path {datapath}."

    dataprocessor1 = DataProcessor()
    _ = dataprocessor1.import_csv_data(datapath)

    # First, identify and remove initial set of outliers
    outlier_index_list = dataprocessor1.identify_outliers(fit_mode = 1)
    df_denoise = dataprocessor1.remove_outliers(outlier_index_list)
    dataprocessor1.update_data(df_denoise)
    num_outliers_removed = len(outlier_index_list)

    # Then, refit the data iteratively until all outliers have been removed
    found_all_outliers = False
    while found_all_outliers is False:

        outlier_index_list = dataprocessor1.identify_outliers_iterative(fit_mode = 1)

        if len(outlier_index_list) == 0:
            found_all_outliers = True
        else:
            num_outliers_removed += len(outlier_index_list)
            df_denoise = dataprocessor1.remove_outliers(outlier_index_list)
            dataprocessor1.update_data(df_denoise)

    assert num_outliers_removed == 2, f"FAILED Parabola Outliers Test 1.  Number of outliers: {num_outliers_removed}, Expected: {2}."

def test_parabola_outliers2():
    '''
    <insert necessary documentation here>
    '''
    datapath = r"Data_Files/parabola2.csv"
    assert os.path.exists(datapath), f"FAILED to locate file path {datapath}."

    dataprocessor1 = DataProcessor()
    _ = dataprocessor1.import_csv_data(datapath)

    # First, identify and remove initial set of outliers
    outlier_index_list = dataprocessor1.identify_outliers(fit_mode = 1)
    df_denoise = dataprocessor1.remove_outliers(outlier_index_list)
    dataprocessor1.update_data(df_denoise)
    num_outliers_removed = len(outlier_index_list)

    # Then, refit the data iteratively until all outliers have been removed
    found_all_outliers = False
    while found_all_outliers is False:

        outlier_index_list = dataprocessor1.identify_outliers_iterative(fit_mode = 1)

        if len(outlier_index_list) == 0:
            found_all_outliers = True
        else:
            num_outliers_removed += len(outlier_index_list)
            df_denoise = dataprocessor1.remove_outliers(outlier_index_list)
            dataprocessor1.update_data(df_denoise)

    assert num_outliers_removed == 3, f"FAILED Parabola Outliers Test 1.  Number of outliers: {num_outliers_removed}, Expected: {3}."
