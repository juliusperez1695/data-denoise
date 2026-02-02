'''
data_denoise.py

Description: This class defines the High-level functionality of the Data Denoise application.
'''

from time import sleep
from data_processor import DataProcessor
from solution_checker import SolutionChecker

################################
#~DataDenoiser CLASS defintion~#
################################
class DataDenoiser:
    '''
    A class for initiating actions requested by the user and for performing the high-level functions
    which are expected of the application.
    '''
    def __init__(self):
        self.dataprocessor = DataProcessor()
        self.fit_mode = 0

    def import_data(self):
        ''' Calls the necessary function for importing user data '''
        valid_path = False
        while not valid_path:
            try:
                self.dataprocessor.import_csv_data(self.get_data_filepath())
                valid_path = True
            except(FileNotFoundError, IOError):
                print("Invalid File Path - try again.")
                continue
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
        # First, identify and remove initial set of outliers
        outlier_index_list = self.dataprocessor.identify_outliers(fit_mode)
        df_denoise = self.dataprocessor.remove_outliers(outlier_index_list)
        self.dataprocessor.update_data(df_denoise)
        num_outliers_removed = len(outlier_index_list)

        # Then, refit the data iteratively until all outliers have been removed
        found_all_outliers = False
        while found_all_outliers is False:

            outlier_index_list = self.dataprocessor.identify_outliers_iterative(fit_mode)

            if len(outlier_index_list) == 0:
                found_all_outliers = True
            else:
                num_outliers_removed += len(outlier_index_list)
                df_denoise = self.dataprocessor.remove_outliers(outlier_index_list)
                self.dataprocessor.update_data(df_denoise)
        print("\nNumber of Outliers Removed: " + str(num_outliers_removed) + "\n\n")
        sleep(1.5)
        print("Return to Data Processing Menu to check solution.")

        self.fit_mode = fit_mode
        sleep(4)

        return num_outliers_removed

    def run_solution_check(self):
        '''
        Compares and validates the processed solution against:
        - original data
        - expected solution
        '''
        # Obtain the fit parameters for before and after outlier removal
        _, init_fit_params = self.dataprocessor.get_init_fit_results()
        _, denoise_fit_params = self.dataprocessor.get_denoise_fit_results()

        #Creates SolutionChecker object for comparing key points derived from parameter values
        solution_check = SolutionChecker(init_fit_params, denoise_fit_params, self.fit_mode)

        # Report comparison between initial fit and denoised fit
        results_table = solution_check.run_comparison()

        #Display and Export Results
        print("\n")
        print(results_table)
        print("\n")
        print("The table above has been saved here: './output_csv_reports/'")
        self.dataprocessor.export_csv_report(results_table, "results_comparison")

        # Plot comparison and generate csv report
        self.dataprocessor.plot_data(export_plot=True)

        init_df = self.dataprocessor.get_orig_data()
        final_df = self.dataprocessor.get_denoise_data()
        data_csv_report = solution_check.build_compare_df(init_df, final_df)
        self.dataprocessor.export_csv_report(data_csv_report, "plot_data_comparison")
        print("Solution Data (before and after outlier removal) has been saved here: ")
        print("     './output_csv_reports/'\n\n")
        print("Returning to Data Processing Menu . . . ")
        sleep(4)
