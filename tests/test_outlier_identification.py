'''
<insert necessary documentation here>
'''

import os
import pandas as pd
from data_processor import DataProcessor
from data_denoise import Denoiser

def test_parabola_outliers():
    '''
    <insert necessary documentation here>
    '''
    datapath = r"Data_Files/parabola1.csv"
    assert os.path.exists(datapath), f"FAILED to locate file path {datapath}."

    test_df = pd.read_csv(datapath, header=None, float_precision='round_trip')
    dataprocessor1 = DataProcessor()
    dataprocessor1.set_orig_data(test_df)

    denoiser1 = Denoiser()
    # outlier_idxs = dataprocessor.identify_outliers_iterative(fit_mode = 1)
    num_outliers = denoiser1.run_outlier_removal(fit_mode = 1)# len(outlier_idxs)

    assert num_outliers == 2, f"FAILED Parabola Outliers Test 1.  Number of outliers: {num_outliers}, Expected: {2}."

    datapath = r"Data_Files/parabola2.csv"
    assert os.path.exists(datapath), f"FAILED to locate file path {datapath}."

    test_df = pd.read_csv(datapath, header=None, float_precision='round_trip')
    dataprocessor2 = DataProcessor()
    dataprocessor2.set_orig_data(test_df)

    denoiser2 = Denoiser()
    # outlier_idxs = dataprocessor.identify_outliers_iterative(fit_mode = 1)
    num_outliers = denoiser2.run_outlier_removal(fit_mode = 1) # len(outlier_idxs)

    assert num_outliers == 3, f"FAILED Parabola Outliers Test 2.  Number of outliers: {num_outliers}, Expected: {3}."