from time import sleep
from DataProcessor import *
from SolutionChecker import *

################################
#~DataDenoiser CLASS defintion~#
################################
class DataDenoiser:
    def __init__(self):
        self.dataprocessor = DataProcessor()
        self.fit_mode = 0

    def importData(self):
        self.dataprocessor.importCSVdata(self.getDataFilepath())
        print("\nSuccessfully imported data!")
        sleep(1.5)
    
    def getDataFilepath(self):
        datapath = input("\nEnter the complete file path for your dataset: ")
        return datapath
    
    def Run_Plotter(self):
        self.dataprocessor.plotData()
    
    def Run_OutlierRemoval(self, fit_mode : int = 1):
        outlierIndexList = self.dataprocessor.identifyOutliers(fit_mode)
        df_denoise = self.dataprocessor.removeOutliers(outlierIndexList)
        print("\nNumber of Outliers Removed: " + str(len(outlierIndexList)) + "\n\n")
        sleep(1.5)
        print("Return to Data Processing Menu to check solution.")
        self.dataprocessor.updateData(df_denoise)

        self.fit_mode = fit_mode
        sleep(4)

    def Run_SolutionCheck(self):
        #Fit cleaned data, Fit original data, and compare key values (max/min values and locations)
        df = self.dataprocessor.getOrigData()
        y_dfFit = self.dataprocessor.getInitFitResults()
        
        df_denoise = self.dataprocessor.getDenoiseData()
        fit_type = self.dataprocessor.getFitType(self.fit_mode)
        y_dfDenoiseFit = self.dataprocessor.getFitValues(fit_type, df_denoise.iloc[:,0], df_denoise.iloc[:,1])
        
        #Creates SolutionChecker object for performing fitting method and locating extrema
        solution_check = SolutionChecker(y_dfFit, y_dfDenoiseFit)
        
        #Find extrema of original data fit and clean data fit along with indices
        df_idx, df_Extrema = solution_check.findExtrema(y_dfFit)
        df_denoise_idx, df_denoise_Extrema = solution_check.findExtrema(y_dfDenoiseFit)
        
        #Display Results
        print("\nOriginal Extrema: " + str(df_Extrema))
        print("Original Extrema Location: " + str(df.iloc[:,0].iloc[df_idx]))
        print("Denoised Extrema: " + str(df_denoise_Extrema))
        print("Denoised Extrema Location: " + str(df_denoise.iloc[:,0].iloc[df_denoise_idx]) + "\n\n")
        self.dataprocessor.plotData()
        print("\n\nReturning to Data Processing Menu . . . ")
        sleep(4)

