''' The purpose of this module is to perform operations on the uploaded data '''

import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from time import sleep

from numpy import typing as npt
from typing import List

class DataProcessor:
    def __init__(self):
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        self.init_fit_results = np.array([])

    def import_csv_data(self, data_file_path : str):
        # clear dataframes for each new import
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        df = pd.read_csv(data_file_path, header=None, float_precision='round_trip')

        self.orig_df = df
        self.new_df = df

        return df

    def plot_data(self):
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
        N = np.size(fit_values)
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

        currIdx = 0
        for d in dist2fit:
            if d/rss > 20:
                self.idx_list.append(currIdx)
            currIdx += 1
        return self.idx_list

    def remove_outliers(self, outlier_loc : List[int]):
        for loc in outlier_loc:
            self.new_df = self.new_df.drop(loc)
        return self.new_df

    def parabola_fit(self, x, a, b, c):
        return a + b*x + c*x**2

    def get_fit_values(self, fitType, xValues, yValues):
        popt, pcov = curve_fit(fitType, xValues, yValues)
        return self.parabola_fit(xValues, *popt)

    def get_fit_type(self, fit_mode : int):
        if fit_mode == 1:
            fit_type = self.parabola_fit
        else:
            fit_type = self.parabola_fit

        return fit_type

    def reset_idx_list(self):
        self.idx_list = []

    def update_data(self, df):
        self.new_df = df

    def remove_data(self, x_value):
        self.new_df = self.new_df.drop(x_value, axis='index')

    def print_data(self):
        print(self.new_df)

    def get_denoise_data(self):
        return self.new_df

    def get_orig_data(self):
        return self.orig_df

    def get_init_fit_results(self):
        return self.init_fit_results

    def set_orig_data(self, input_df):
        self.orig_df = input_df