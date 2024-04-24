''' The purpose of this module is to perform operations on the uploaded data '''

import matplotlib.pyplot as plt

class DataProcessor:
	def __init__(self, inputDF):
		self.origDF = inputDF
		self.newDF = inputDF

	def plotData(self):
		plt.figure(figsize=(9,5))
		
		plt.subplot(121)
		plt.plot(self.origDF['x'], self.origDF['y'], 'ro')
		plt.title('Original Data')
		plt.xlabel('x values')
		plt.ylabel('y values')

		plt.subplot(122)
		plt.plot(self.newDF['x'], self.newDF['y'], 'bo')
		plt.title('Processed Data')
		plt.xlabel('x values')
		plt.ylabel('y values')

		plt.show()

	def updateData(self, df):
		self.newDF = df

	def removeData(self, x_value):
		self.newDF = self.newDF.drop(x_value, axis='index')

	def printData(self):
		print(self.newDF)

	def getCleanData():
		return self.newDF

	def getOrigData():
		return self.origDF