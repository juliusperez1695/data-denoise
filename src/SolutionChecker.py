import matplotlib.pyplot as plt

class SolutionChecker:
	def __init__(self, data, denoiseData):
		self.origFit = data
		self.denoiseFit = denoiseData

	def findExtrema(self, input):
		if self.denoiseFit[0] > self.denoiseFit[5]:
			return input.idxmin(), input.min()
		else:
			return input.idxmax(), input.max()

	def plotSummary(self, orig_df, denoise_df):
		print("**Close plot window to continue**\n\n")
		plt.figure(figsize=(9,5))
		
		plt.subplot(121)
		plt.plot(orig_df.iloc[:,0], self.origFit, 'r-')
		plt.plot(orig_df.iloc[:,0], orig_df.iloc[:,1], 'ro')
		plt.title('Original Data')
		plt.xlabel('x values')
		plt.ylabel('y values')
		plt.legend(['Fit','Data'])

		plt.subplot(122)
		plt.plot(denoise_df.iloc[:,0], self.denoiseFit, 'b-')
		plt.plot(denoise_df.iloc[:,0], denoise_df.iloc[:,1], 'bo')
		plt.title('Processed Data')
		plt.xlabel('x values')
		plt.ylabel('y values')
		plt.legend(['Fit','Data'])

		plt.show()