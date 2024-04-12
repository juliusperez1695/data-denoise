import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

class StatisticsLibrary:
	idxList = []

	def __init__(self, data):
		self.df = data

	def identifyOutliers(self):
		#Fits the original data using Nonlinear Regression Parabolic Fitting
		#Identifies outliers based on original data's distance from fit value
		fit_Yvalues = self.getFitValues(self.parabolaFit, self.df['x'], self.df['y'])
		dist2fit = abs(fit_Yvalues - self.df['y'])
		currIdx = 0
		for d in dist2fit:
			if d > 10:
				self.idxList.append(currIdx)
			currIdx += 1
		return self.idxList
	
		
	def removeOutliers(self, outlierLoc):
		for loc in outlierLoc:
			self.df = self.df.drop(loc)
		return self.df

	def parabolaFit(self, x, a, b, c):
		return a + b*x + c*x**2

	def getFitValues(self, fitType, xValues, yValues):
		popt, pcov = curve_fit(fitType, xValues, yValues)
		return self.parabolaFit(xValues, *popt)

	def resetIdxList(self):
		self.idxList = []