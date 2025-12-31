''' The purpose of this module is to perform operations on the uploaded data '''

import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from time import sleep

from numpy import typing as npt
from typing import List

class DataProcessor:
    '''
    Creates an object for handling and processing datasets
    '''
    def __init__(self):
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        self.init_fit_results = np.array([])

    def import_csv_data(self, data_file_path : str):
        '''
        <insert necessary documentation here>
        '''
        # clear dataframes for each new import
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        df = pd.read_csv(data_file_path, header=None, float_precision='round_trip')

        self.orig_df = df
        self.new_df = df

        return df

    def plot_data(self):
        '''
        <insert necessary documentation here>
        '''
        plt.figure(figsize=(9,5))

        plt.subplot(121)
        plt.plot(self.orig_df.iloc[:,0], self.orig_df.iloc[:,1], 'ro')
        plt.title('Original Data')
        plt.xlabel('x values')
        plt.ylabel('y values')

        plt.subplot(122)
        plt.plot(self.new_df.iloc[:,0], self.new_df.iloc[:,1], 'bo')
        plt.title('Processed Data')
        plt.xlabel('x values')
        plt.ylabel('y values')

        print("**Close plot window to continue**\n\n")

        plt.show()

    def calculate_rss(self, fit_values : npt.NDArray[np.float64], data_values : npt.NDArray[np.float64]):
        '''
        <insert necessary documentation here>
        '''
        residuals = fit_values - data_values
        rss = np.sqrt(np.sum(residuals**2))

        return rss

    def identify_outliers(self, fit_mode : int = 1):
        '''
        - Fits the original data using the preferred fitting method specified by fit_mode
        - Identifies outliers based on Residual Sum of Squares (RSS) of original data
            and compares to each data point's distance from the corresponding fit value
        '''
        fit_type = self.get_fit_type(fit_mode)
        orig_df_x = self.orig_df.iloc[:,0]
        orig_df_y = self.orig_df.iloc[:,1]
        self.init_fit_results = self.get_fit_values(fit_type, orig_df_x, orig_df_y)
        dist2fit = abs(100*(self.init_fit_results - orig_df_y))
        rss = self.calculate_rss(self.init_fit_results, np.array(orig_df_y))

        curr_idx = 0
        for d in dist2fit:
            if d/rss > 20:
                self.idx_list.append(curr_idx)
            curr_idx += 1
        return self.idx_list

    def remove_outliers(self, outlier_loc : List[int]):
        '''
        <insert necessary documentation here>
        '''
        for loc in outlier_loc:
            self.new_df = self.new_df.drop(loc)
        return self.new_df

    def parabola_fit(self, x, a, b, c):
        '''
        <insert necessary documentation here>
        '''
        return a + b*x + c*x**2

    def get_fit_values(self, fit_type, x_values, y_values):
        '''
        <insert necessary documentation here>
        '''
        popt, pcov = curve_fit(fit_type, x_values, y_values)
        return self.parabola_fit(x_values, *popt)

    def get_fit_type(self, fit_mode : int):
        '''
        <insert necessary documentation here>
        '''
        if fit_mode == 1:
            fit_type = self.parabola_fit
        else:
            fit_type = self.parabola_fit

        return fit_type

    def reset_idx_list(self):
        '''
        <insert necessary documentation here>
        '''
        self.idx_list = []

    def update_data(self, df):
        '''
        <insert necessary documentation here>
        '''
        self.new_df = df

    def remove_data(self, x_value):
        '''
        <insert necessary documentation here>
        '''
        self.new_df = self.new_df.drop(x_value, axis='index')

    def print_data(self):
        '''
        <insert necessary documentation here>
        '''
        print(self.new_df)

    def get_denoise_data(self):
        '''
        <insert necessary documentation here>
        '''
        return self.new_df

    def get_orig_data(self):
        '''
        <insert necessary documentation here>
        '''
        return self.orig_df

    def get_init_fit_results(self):
        '''
        <insert necessary documentation here>
        '''
        return self.init_fit_results

    def set_orig_data(self, input_df):
        '''
        <insert necessary documentation here>
        '''
        self.orig_df = input_df
