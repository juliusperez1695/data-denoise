import matplotlib.pyplot as plt

class SolutionChecker:
	def __init__(self, data, cleanData):
		self.origFit = data
		self.cleanFit = cleanData

	def findExtrema(self, input):
		if self.cleanFit[0] > self.cleanFit[5]:
			return input.idxmin(), input.min()
		else:
			return input.idxmax(), input.max()

	def plotSummary(self, orig_df, clean_df):
		print("**Close plot window to continue**\n\n")
		plt.figure(figsize=(9,5))
		
		plt.subplot(121)
		plt.plot(orig_df['x'], self.origFit, 'r-')
		plt.plot(orig_df['x'], orig_df['y'], 'ro')
		plt.title('Original Data')
		plt.xlabel('x values')
		plt.ylabel('y values')
		plt.legend(['Fit','Data'])

		plt.subplot(122)
		plt.plot(clean_df['x'], self.cleanFit, 'b-')
		plt.plot(clean_df['x'], clean_df['y'], 'bo')
		plt.title('Processed Data')
		plt.xlabel('x values')
		plt.ylabel('y values')
		plt.legend(['Fit','Data'])

		plt.show()