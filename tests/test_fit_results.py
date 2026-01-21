'''
<insert necessary documentation here>
'''

import numpy as np
import pandas as pd
from data_processor import DataProcessor

def test_parabola_fit():
    '''
    <insert necessary documentation here>
    '''
    # Generate test values
    x_vals = np.arange(0, 20, 0.5)
    test_coeffs = np.array([10., 10., 5.])
    y_vals = test_coeffs[2]*x_vals**2 + test_coeffs[1]*x_vals + test_coeffs[0]
    df_test = pd.DataFrame()
    df_test[0] = x_vals
    df_test[1] = y_vals

    # Generate fit values
    dataprocessor = DataProcessor()
    dataprocessor.set_orig_data(df_test)
    fit_type = dataprocessor._get_fit_type(fit_mode = 1)
    _, fit_params = dataprocessor.get_fit_values(fit_type, x_vals, y_vals)

    assert (test_coeffs == fit_params).all(), f"FAILED Parabola Fit. Coefficients (Fit) = {test_coeffs}, Coefficients (Expected) = {fit_params}."
