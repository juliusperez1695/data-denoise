''' This file will prompt the user for input,  asking for the folder path containing 
	the data file.  It will then call on the required modules to perform data cleaning. '''

import pandas as pd
from DataProcessor import *
from StatisticsLibrary import *
from SolutionChecker import *
from SQLServerImportSet1 import *
from SQLServerImportSet2 import *


def displayMenu():
	menu = {1:"Plot current data", 2:"Handle Outliers", 3:"Check Solution", 4:"Load New Data", 5:"Exit Program"}
	print("########")
	print("# MENU #")
	print("########")

	for choice in menu:
		print(str(choice) + " " + menu[choice])

def loadData(fileName):
	df = pd.read_csv(fileName, header=None)
	df.columns = ['x','y']
	print(df)
	print("\nData upload successful!\n")

	#Read csv file and import to specific db table based on user input
	import1 = SQLServerImportSet1
	import2 = SQLServerImportSet2
	
	if fileName == "Dataset1.csv":
		import1.import_csv_tosql()
	else:
		import2.import_csv_tosql()

	return df

def main():

	print("WELCOME TO THE DATA CLEANER!")
	fileName = input("\nEnter the File Name for the data to be processed: ")

	#Read CSV file into a pandas Data Frame
	df = loadData(fileName)

	#Creates DataProcessor object for performing operations on the Data Frame
	DP = DataProcessor(df)
	#Creates StatisicsLibrary object for fitting data and dealing with outliers
	SL = StatisticsLibrary(df)

	menuChoice = 0
	while(menuChoice != 5):
		displayMenu()
		menuChoice = int(input("\nChoose what to do next: "))

		match menuChoice:
			case 1:
				print("**Close plot window to continue**\n\n")
				DP.plotData()
			case 2:
				#Handle Outliers using Statistics Library
				outlierIndexList = SL.identifyOutliers()
				df_clean = SL.removeOutliers(outlierIndexList)
				print("\nNumber of Outliers Removed: " + str(len(outlierIndexList)) + "\n\n")
				DP.updateData(df_clean)
			case 3:
				#Fit cleaned data, Fit original data, and compare key values (max/min values and locations)
				y_dfFit = SL.getFitValues(SL.parabolaFit, df['x'], df['y'])
				y_dfCleanFit = SL.getFitValues(SL.parabolaFit, df_clean['x'], df_clean['y'])
				
				#Creates SolutionChecker object for performing fitting method and locating extrema
				SC = SolutionChecker(y_dfFit, y_dfCleanFit)
				
				#Find extrema of original data fit and clean data fit along with indices
				df_idx, df_Extrema = SC.findExtrema(y_dfFit)
				df_clean_idx, df_clean_Extrema = SC.findExtrema(y_dfCleanFit)
				
				#Display Results
				print("\nOriginal Extrema: " + str(df_Extrema))
				print("Orginal Extrema Location: " + str(df['x'].iloc[df_idx]))
				print("Cleaned Extrema: " + str(df_clean_Extrema))
				print("Cleaned Extrema Location: " + str(df_clean['x'].iloc[df_clean_idx]) + "\n\n")
				SC.plotSummary(df, df_clean)
			case 4:
				fileName = input("\nEnter the File Name for the data to be processed: ")
				df = loadData(fileName)
				DP = DataProcessor(df)
				SL = StatisticsLibrary(df)
				SL.resetIdxList()
			case 5:
				print("Program Terminated.\n\n")

#RUN PROGRAM
main()

