'''
<insert necessary documentation here>
'''

from time import sleep
from data_processor import DataProcessor
from solution_checker import SolutionChecker

################################
#~DataDenoiser CLASS defintion~#
################################
class DataDenoiser:
    '''
    <insert necessary documentation here>
    '''
    def __init__(self):
        self.dataprocessor = DataProcessor()
        self.fit_mode = 0

    def import_data(self):
        ''' Calls the necessary function for importing user data '''
        self.dataprocessor.import_csv_data(self.get_data_filepath())
        print("\nSuccessfully imported data!")
        sleep(1.5)

    def get_data_filepath(self):
        ''' Prompts the user for a complete file path ending with file extension '.csv' '''
        datapath = input("\nEnter the complete file path for your dataset: ")
        return datapath

    def run_plotter(self):
        ''' Plots the user's imported data alongside the processed data '''
        self.dataprocessor.plot_data()

    def run_outlier_removal(self, fit_mode : int = 1):
        ''' Removes outliers based on fit-type used (specified by fit_mode) '''
        outlier_index_list = self.dataprocessor.identify_outliers(fit_mode)
        df_denoise = self.dataprocessor.remove_outliers(outlier_index_list)
        print("\nNumber of Outliers Removed: " + str(len(outlier_index_list)) + "\n\n")
        sleep(1.5)
        print("Return to Data Processing Menu to check solution.")
        self.dataprocessor.update_data(df_denoise)

        self.fit_mode = fit_mode
        sleep(4)

    def run_solution_check(self):
        ''' Compares and validates the processed solution against the original data and expected solution '''
        #Fit cleaned data, Fit original data, and compare key values (max/min values and locations)
        df = self.dataprocessor.get_orig_data()
        y_df_fit = self.dataprocessor.get_init_fit_results()

        df_denoise = self.dataprocessor.get_denoise_data()
        df_denoise_x = df_denoise.iloc[:,0]
        df_denoise_y = df_denoise.iloc[:,1]
        fit_type = self.dataprocessor.get_fit_type(self.fit_mode)
        y_df_denoise_fit = self.dataprocessor.get_fit_values(fit_type, df_denoise_x, df_denoise_y)

        #Creates SolutionChecker object for performing fitting method and locating extrema
        solution_check = SolutionChecker(y_df_fit, y_df_denoise_fit)

        #Find extrema of original data fit and clean data fit along with indices
        df_idx, df_extrema = solution_check.find_extrema(y_df_fit)
        df_denoise_idx, df_denoise_extrema = solution_check.find_extrema(y_df_denoise_fit)

        #Display Results
        print("\nOriginal Extrema: " + str(df_extrema))
        print("Original Extrema Location: " + str(df.iloc[:,0].iloc[df_idx]))
        print("Denoised Extrema: " + str(df_denoise_extrema))
        print("Denoised Extrema Location: " + str(df_denoise_x.iloc[df_denoise_idx]) + "\n\n")
        self.dataprocessor.plot_data()
        print("Returning to Data Processing Menu . . . ")
        sleep(4)
