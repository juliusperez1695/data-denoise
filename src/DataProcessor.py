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
		self.idxList = []
		self.origDF = pd.DataFrame()
		self.newDF = pd.DataFrame()
		self.init_fit_results = np.array([])

	def importCSVdata(self, data_file_path : str):
		# clear dataframes for each new import
		self.idxList = []
		self.origDF = pd.DataFrame()
		self.newDF = pd.DataFrame()
		df = pd.read_csv(data_file_path, header=None, float_precision='round_trip')

		self.origDF = df
		self.newDF = df

		return df
	
	def plotData(self):
		plt.figure(figsize=(9,5))
		
		plt.subplot(121)
		plt.plot(self.origDF.iloc[:,0], self.origDF.iloc[:,1], 'ro')
		plt.title('Original Data')
		plt.xlabel('x values')
		plt.ylabel('y values')

		plt.subplot(122)
		plt.plot(self.newDF.iloc[:,0], self.newDF.iloc[:,1], 'bo')
		plt.title('Processed Data')
		plt.xlabel('x values')
		plt.ylabel('y values')

		print("**Close plot window to continue**\n\n")
		
		plt.show()

	def calculateRSS(self, fit_values : npt.NDArray[np.float64], data_values : npt.NDArray[np.float64]):
		N = np.size(fit_values)
		residuals = fit_values - data_values
		rss = np.sqrt(np.sum(residuals**2))

		return rss
	
	def identifyOutliers(self, fit_mode : int = 1):
		'''
		- Fits the original data using the preferred fitting method specified by fit_mode
		- Identifies outliers based on Residual Sum of Squares (RSS) of original data 
			and compares to each data point's distance from the corresponding fit value
		'''
		fit_type = self.getFitType(fit_mode)
		self.init_fit_results = self.getFitValues(fit_type, self.origDF.iloc[:,0], self.origDF.iloc[:,1])
		dist2fit = abs(100*(self.init_fit_results - (self.origDF.iloc[:,1])))
		rss = self.calculateRSS(self.init_fit_results, np.array(self.origDF.iloc[:,1]))
		# print(pd.DataFrame(list(zip(fit_Yvalues, self.origDF.iloc[:,1].to_list(), dist2fit/rss))))
		# print(f"RSS = {rss}")
		currIdx = 0
		for d in dist2fit:
			if d/rss > 20:
				self.idxList.append(currIdx)
			currIdx += 1
		return self.idxList
		
	def removeOutliers(self, outlierLoc : List[int]):
		for loc in outlierLoc:
			self.newDF = self.newDF.drop(loc)
		return self.newDF

	def parabolaFit(self, x, a, b, c):
		return a + b*x + c*x**2

	def getFitValues(self, fitType, xValues, yValues):
		popt, pcov = curve_fit(fitType, xValues, yValues)
		return self.parabolaFit(xValues, *popt)

	def getFitType(self, fit_mode : int):
		match fit_mode:
			case 1:
				fit_type = self.parabolaFit
			case _:
				fit_type = self.parabolaFit

		return fit_type
	
	def resetIdxList(self):
		self.idxList = []
	
	def updateData(self, df):
		self.newDF = df

	def removeData(self, x_value):
		self.newDF = self.newDF.drop(x_value, axis='index')

	def printData(self):
		print(self.newDF)

	def getDenoiseData(self):
		return self.newDF

	def getOrigData(self):
		return self.origDF
	
	def getInitFitResults(self):
		return self.init_fit_results
	
	def setOrigData(self, input_df):
		self.origDF = input_df