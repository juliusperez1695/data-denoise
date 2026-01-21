'''
<insert necessary documentation here>
'''

import os
import pandas as pd
from data_processor import DataProcessor

def test_parabola_outliers():
    '''
    <insert necessary documentation here>
    '''
    datapath = r"Data_Files/parabola1.csv"
    assert os.path.exists(datapath), f"FAILED to locate file path {datapath}."

    test_df = pd.read_csv(datapath, header=None, float_precision='round_trip')
    dataprocessor1 = DataProcessor()
    dataprocessor1.set_orig_data(test_df)

    # First, identify and remove initial set of outliers
    outlier_index_list = dataprocessor1.identify_outliers(fit_mode = 1)
    df_denoise = dataprocessor1.remove_outliers(outlier_index_list)
    dataprocessor1.update_data(test_df)
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
