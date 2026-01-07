''' The purpose of this module is to perform operations on the uploaded data '''

from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from numpy import typing as npt

class DataProcessor:
    '''
    Creates an object for handling and processing datasets
    '''
    def __init__(self):
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        self.init_fit_results = np.array([])
        self.init_fit_params = np.array([])
        self.denoise_fit_results = np.array([])
        self.denoise_fit_params = np.array([])

    def import_csv_data(self, data_file_path : str):
        '''
        <insert helpful documentation here>
        '''
        # clear dataframes for each new import
        self.idx_list = []
        self.orig_df = pd.DataFrame()
        self.new_df = pd.DataFrame()
        self.init_fit_results = np.array([])
        self.init_fit_params = np.array([])
        self.denoise_fit_results = np.array([])
        self.denoise_fit_params = np.array([])
        df = pd.read_csv(data_file_path, header=None, float_precision='round_trip')

        self.orig_df = df
        self.new_df = df

        return df

    def plot_data(self):
        '''
        <insert helpful documentation here>
        '''
        plt.figure(figsize=(12,5))

        plt.subplot(121)
        plt.plot(self.orig_df.iloc[:,0], self.orig_df.iloc[:,1], 'ko')
        if np.size(self.init_fit_results) != 0:
            plt.plot(self.orig_df.iloc[:,0], self.init_fit_results, 'r--')
        plt.title('Original Data')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        if np.size(self.init_fit_results) != 0:
            plt.legend(["Orig. Data", "Orig. Fit"])

        plt.subplot(122)
        plt.plot(self.new_df.iloc[:,0], self.new_df.iloc[:,1], 'bo')
        if np.size(self.denoise_fit_results) != 0:
            plt.plot(self.new_df.iloc[:,0], self.denoise_fit_results, '--', color='orange')
        plt.title('Processed Data')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        if np.size(self.denoise_fit_results) != 0:
            plt.legend(["Denoised Data", "Denoised Fit"])

        print("**Close plot window to continue**\n\n")

        plt.show()

    def calculate_rss(
        self, fit_values : npt.NDArray[np.float64],
        data_values : npt.NDArray[np.float64]
    ):
        '''
        <insert helpful documentation here>
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
        self.init_fit_results, self.init_fit_params = self.get_fit_values(fit_type, orig_df_x, orig_df_y)
        dist2fit = abs(100*(self.init_fit_results - orig_df_y))
        rss = self.calculate_rss(self.init_fit_results, np.array(orig_df_y))

        curr_idx = 0
        for d in dist2fit:
            if d/rss > 20:
                self.idx_list.append(curr_idx)
            curr_idx += 1
        return self.idx_list

    def identify_outliers_iterative(self, fit_mode : int = 1):
        '''
        - Fits the NEW data using the preferred fitting method specified by fit_mode
        - Identifies outliers based on Residual Sum of Squares (RSS) of original data
            and compares to each data point's distance from the corresponding fit value
        '''
        fit_type = self.get_fit_type(fit_mode)
        fit_tolerance = self.get_fit_tolerance(fit_mode)
        df_x = self.new_df.iloc[:,0]
        df_y = self.new_df.iloc[:,1]
        self.denoise_fit_results, self.denoise_fit_params = self.get_fit_values(fit_type,
                                                                                df_x,
                                                                                df_y)
        dist2fit = abs(100*(self.denoise_fit_results - df_y))
        rss = self.calculate_rss(self.denoise_fit_results, np.array(df_y))

        curr_idx = 0
        self.idx_list = []
        for d in dist2fit:
            if d/rss > fit_tolerance:
                self.idx_list.append(curr_idx)
            curr_idx += 1
        return self.idx_list

    def remove_outliers(self, outlier_loc : List[int]):
        '''
        <insert helpful documentation here>
        '''
        for loc in outlier_loc:
            self.new_df = self.new_df.drop(loc)
        self.new_df = self.new_df.reset_index(drop=True)
        return self.new_df

    def parabola_fit(self, x, a, b, c):
        '''
        Docstring for parabola_fit

        :param x: Independent variable
        :param a: Constant coefficient
        :param b: Linear coefficient
        :param c: Square coefficient
        '''
        return a + b*x + c*x**2

    def guess_parabola_params(self, x_data, y_data) -> np.ndarray:
        '''
        Docstring for guess_parabola_params

        :param x_data: Description
        :param y_data: Description
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        '''
        a = 1
        b = 1
        c = 1

        return np.array([a, b, c])

    def sigmoid_fit(self, x, a, b, c, d):
        '''
        Docstring for sigmoid_fit

        :param x: independent variable
        :param a: Vertical scale-factor
        :param b: Horizontal scale-factor
        :param c: Delay constant
        :param d: Offset
        '''
        np.seterr(over='ignore')
        return a / (1 + np.exp(-b*(x - c))) + d

    def guess_sigmoid_params(self, x_data, y_data) -> np.ndarray:
        '''
        Docstring for guess_sigmoid_params

        :param x_data: Description
        :param y_data: Description
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        '''
        a = np.max(y_data)
        b = 1.0
        c = x_data[len(y_data) // 2]
        d = np.min(y_data)

        return np.array([a, b, c, d])

    def linear_fit(self, x, a, b):
        '''
        Docstring for linear_fit

        :param x: independent variable
        :param a: Slope
        :param b: y-intercept
        '''
        return a*x + b

    def exponential_fit(self, x, a, b, c, d):
        '''
        Docstring for exponential_fit

        :param x: Independent variable
        :param a: Vertical scale-factor
        :param b: Horizontal scale-factor
        :param c: Delay constant
        :param d: Offset
        '''
        return a*np.exp(b*(x - c)) + d

    def guess_exp_params(self, x_data, y_data) -> np.ndarray:
        '''
        Docstring for guess_exp_params

        :param x_data: Description
        :param y_data: Description
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        '''

    def get_fit_values(self, fit_type, x_values, y_values):
        '''
        <insert helpful documentation here>
        '''

        if fit_type == self.parabola_fit:
            initial_guesses = self.guess_parabola_params(x_values, y_values)
            popt, _ = curve_fit(fit_type, x_values, y_values, p0=initial_guesses)
            fit_values = self.parabola_fit(x_values, *popt)
        elif fit_type == self.sigmoid_fit:
            initial_guesses = self.guess_sigmoid_params(x_values, y_values)
            popt, _ = curve_fit(fit_type, x_values, y_values, p0=initial_guesses)
            fit_values = self.sigmoid_fit(x_values, *popt)
        elif fit_type == self.linear_fit:
            initial_guesses = [1, 0]
            popt, _ = curve_fit(fit_type, x_values, y_values, p0=initial_guesses)
            fit_values = self.linear_fit(x_values, *popt)
        elif fit_type == self.exponential_fit:
            initial_guesses = []
            popt, _ = curve_fit(fit_type, x_values, y_values, p0=initial_guesses)
            fit_values = self.exponential_fit(x_values, *popt)
        else:
            initial_guesses = []
            popt, _ = curve_fit(fit_type, x_values, y_values, p0=initial_guesses)
            fit_values = self.parabola_fit(x_values, *popt)

        model_params = popt
        return fit_values, model_params

    def get_fit_type(self, fit_mode : int):
        '''
        <insert helpful documentation here>
        '''
        if fit_mode == 1:
            fit_type = self.parabola_fit
        elif fit_mode == 2:
            fit_type = self.sigmoid_fit
        elif fit_mode == 3:
            fit_type = self.linear_fit
        elif fit_mode == 4:
            fit_type = self.exponential_fit
        else:
            fit_type = self.parabola_fit

        return fit_type

    def get_fit_tolerance(self, fit_mode) -> int:
        '''
        Docstring for get_fit_tolerance

        :param fit_mode: Description
        :return: Description
        :rtype: int
        '''
        if fit_mode == 1:
            fit_tolerance = 50
        elif fit_mode == 2:
            fit_tolerance = 20
        elif fit_mode == 3:
            fit_tolerance = 20
        elif fit_mode == 4:
            fit_tolerance = 20
        else:
            fit_tolerance = 20

        return fit_tolerance

    def reset_idx_list(self):
        '''
        <insert helpful documentation here>
        '''
        self.idx_list = []

    def update_data(self, df):
        '''
        <insert helpful documentation here>
        '''
        self.new_df = df

    def remove_data(self, x_value):
        '''
        <insert helpful documentation here>
        '''
        self.new_df = self.new_df.drop(x_value, axis='index')
        self.new_df.reset_index(drop=True)

    def print_data(self):
        '''
        <insert helpful documentation here>
        '''
        print(self.new_df)

    def get_denoise_data(self):
        '''
        <insert helpful documentation here>
        '''
        return self.new_df

    def get_orig_data(self):
        '''
        <insert helpful documentation here>
        '''
        return self.orig_df

    def get_init_fit_results(self):
        '''
        <insert helpful documentation here>
        '''
        return self.init_fit_results, self.init_fit_params

    def set_orig_data(self, input_df):
        '''
        <insert helpful documentation here>
        '''
        self.orig_df = input_df

    def set_denoise_fit_results(self, fit_values):
        '''
        Docstring for set_denoise_fit_results

        :param fit_values: Description
        '''
        self.denoise_fit_results = fit_values
