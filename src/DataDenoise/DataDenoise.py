''' This file will prompt the user for input,  asking for the folder path containing 
	the data file.  It will then call on the required modules to perform data cleaning. '''

import os
from DataProcessor import *
from SolutionChecker import *
from UserInterface import *
# from DB_Configuration import *

def main():
	UI = DataDenoiseUI()
	prog_UI = UI.Initialize()
	UI.RUN()

if __name__ == "__main__":
	main()

class DataDenoiser:
	# dataprocessor = DataProcessor()
	# fit_mode = 0
	
	def __init__(self):
		self.dataprocessor = DataProcessor()
		self.fit_mode = 0
	# Define all functions required
	# 	- Load data
	#	- Plot data
	# 	- Initial Fit and Remove outliers
	#	- Refit and Check solution against expected values
	#	- Export results

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
		SC = SolutionChecker(y_dfFit, y_dfDenoiseFit)
		
		#Find extrema of original data fit and clean data fit along with indices
		df_idx, df_Extrema = SC.findExtrema(y_dfFit)
		df_denoise_idx, df_denoise_Extrema = SC.findExtrema(y_dfDenoiseFit)
		
		#Display Results
		print("\nOriginal Extrema: " + str(df_Extrema))
		print("Original Extrema Location: " + str(df.iloc[:,0].iloc[df_idx]))
		print("Cleaned Extrema: " + str(df_denoise_Extrema))
		print("Cleaned Extrema Location: " + str(df_denoise.iloc[:,0].iloc[df_denoise_idx]) + "\n\n")
		SC.plotSummary(df, df_denoise)

# All of the code BELOW must be objectified using
# the DataDenoiser and UserInterface modules
# def displayMenu():
# 	menu = {1:"Plot current data", 2:"Handle Outliers", 3:"Check Solution", 4:"Load New Data", 5:"Exit Program"}
# 	print("########")
# 	print("# MENU #")
# 	print("########")

# 	for choice in menu:
# 		print(str(choice) + " " + menu[choice])


# def main():
# 	#Clears terminal at program start
# 	os.system('cls' if os.name == 'nt' else 'clear')
	
# 	################################################
	
# 	print("\nWELCOME TO DATA DENOISE!\n")
	
# 	#Prompts User to Provide SQL Server, Database, and DB Table Information for Data Access
# 	DB1 = DB_Configuration()
# 	DB1.getUserConfig()
	
# 	try:
# 		#Stores DB Table into pandas dataframe
# 		df = DB1.getData()
# 		#Creates DataProcessor object for performing operations on the Data Frame
# 		DP = DataProcessor(df)
# 		#Creates StatisicsLibrary object for fitting data and dealing with outliers
# 		SL = StatisticsLibrary(df)
# 		menuChoice = 0
# 	except AttributeError:
# 		print("MESSAGE: Dataset does not exist.\n")
# 		menuChoice = 5
# 		print("Program Terminated.")

# 	while(menuChoice != 5):
# 		displayMenu()
# 		try:
# 			menuChoice = int(input("\nChoose what to do next: "))
# 		except ValueError:
# 			print("ERROR: User did not enter an INTEGER value.\n")
# 			continue

# 		match menuChoice:
# 				case 1:
# 					print("**Close plot window to continue**\n\n")
# 					DP.plotData()
# 				case 2:
# 					#Handle Outliers using Statistics Library
# 					outlierIndexList = SL.identifyOutliers()
# 					df_clean = SL.removeOutliers(outlierIndexList)
# 					print("\nNumber of Outliers Removed: " + str(len(outlierIndexList)) + "\n\n")
# 					DP.updateData(df_clean)
# 				case 3:
# 					#Fit cleaned data, Fit original data, and compare key values (max/min values and locations)
# 					y_dfFit = SL.getFitValues(SL.parabolaFit, df['x'], df['y'])
# 					y_dfCleanFit = SL.getFitValues(SL.parabolaFit, df_clean['x'], df_clean['y'])
					
# 					#Creates SolutionChecker object for performing fitting method and locating extrema
# 					SC = SolutionChecker(y_dfFit, y_dfCleanFit)
					
# 					#Find extrema of original data fit and clean data fit along with indices
# 					df_idx, df_Extrema = SC.findExtrema(y_dfFit)
# 					df_clean_idx, df_clean_Extrema = SC.findExtrema(y_dfCleanFit)
					
# 					#Display Results
# 					print("\nOriginal Extrema: " + str(df_Extrema))
# 					print("Orginal Extrema Location: " + str(df['x'].iloc[df_idx]))
# 					print("Cleaned Extrema: " + str(df_clean_Extrema))
# 					print("Cleaned Extrema Location: " + str(df_clean['x'].iloc[df_clean_idx]) + "\n\n")
# 					SC.plotSummary(df, df_clean)
# 				case 4:
# 					#Re-enters Database for accessing of new dataset
# 					DB1 = DB_Configuration()
# 					DB1.getUserConfig()
# 					df = DB1.getData()
# 					DP = DataProcessor(df)
# 					SL = StatisticsLibrary(df)
# 					SL.resetIdxList()
# 				case 5:
# 					print("Program Terminated.\n\n")
# 				case ValueError():
# 					print("Input error: User did not enter an Integer value.")
# 					print("Program Terminated.")
# 				case _:
# 					print("Invalid Input!\n")

