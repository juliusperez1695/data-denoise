import os
from DataProcessor import *
from SolutionChecker import *
from UserInterface import *

############################################
#~Data Denoise MAIN - Runs the application~#
############################################
def main():
	# Clear terminal at program start
	os.system('cls' if os.name == 'nt' else 'clear')
	
	# Initialize and run the program's user interface
	denoiseUI = DataDenoiseUI()
	prog_UI = denoiseUI.Initialize()
	denoiseUI.RUN(prog_UI)

if __name__ == "__main__":
	main()

################################
#~DataDenoiser CLASS defintion~#
################################
class DataDenoiser:
	
	def __init__(self):
		self.dataprocessor = DataProcessor()
		self.fit_mode = 0

	def importData(self):
		self.dataprocessor.importCSVdata(self.getDataFilepath())
	
	def getDataFilepath(self):
		datapath = input("Enter the complete file path for your dataset: ")
		return datapath
	
	def Run_Plotter(self):
		self.dataprocessor.plotData()
	
	def Run_OutlierRemoval(self, fit_mode : int = 1):
		outlierIndexList = self.dataprocessor.identifyOutliers(fit_mode)
		df_denoise = self.dataprocessor.removeOutliers(outlierIndexList)
		print("\nNumber of Outliers Removed: " + str(len(outlierIndexList)) + "\n\n")
		print("Return to Data Processing Menu to check solution.")
		self.dataprocessor.updateData(df_denoise)

		self.fit_mode = fit_mode

	def Run_SolutionCheck(self):
		#Fit cleaned data, Fit original data, and compare key values (max/min values and locations)
		df = self.dataprocessor.getOrigData()
		df_denoise = self.dataprocessor.getDenoiseData()
		fit_type = self.dataprocessor.getFitType(self.fit_mode)
		y_dfFit = self.dataprocessor.getFitValues(fit_type, df.iloc[:,0], df.iloc[:,1])
		y_dfDenoiseFit = self.dataprocessor.getFitValues(fit_type, df_denoise.iloc[:,0], df_denoise.iloc[:,1])
		
		#Creates SolutionChecker object for performing fitting method and locating extrema
		solution_check = SolutionChecker(y_dfFit, y_dfDenoiseFit)
		
		#Find extrema of original data fit and clean data fit along with indices
		df_idx, df_Extrema = solution_check.findExtrema(y_dfFit)
		df_denoise_idx, df_denoise_Extrema = solution_check.findExtrema(y_dfDenoiseFit)
		
		#Display Results
		print("\nOriginal Extrema: " + str(df_Extrema))
		print("Original Extrema Location: " + str(df.iloc[:,0].iloc[df_idx]))
		print("Cleaned Extrema: " + str(df_denoise_Extrema))
		print("Cleaned Extrema Location: " + str(df_denoise.iloc[:,0].iloc[df_denoise_idx]) + "\n\n")
		solution_check.plotSummary(df, df_denoise)

