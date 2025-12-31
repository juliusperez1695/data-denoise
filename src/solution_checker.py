import matplotlib.pyplot as plt
from data_processor import DataProcessor

class SolutionChecker:
    def __init__(self, data, denoiseData):
        self.origFit = data
        self.denoiseFit = denoiseData

    def findExtrema(self, input):
        if self.denoiseFit[0] > self.denoiseFit[5]:
            return input.idxmin(), input.min()
        else:
            return input.idxmax(), input.max()
