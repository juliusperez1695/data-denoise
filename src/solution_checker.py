import matplotlib.pyplot as plt
from data_processor import DataProcessor

class SolutionChecker:
    '''
    <insert necessary documentation here>
    '''
    def __init__(self, data, denoise_data):
        self.orig_fit = data
        self.denoise_fit = denoise_data

    def find_extrema(self, input):
        '''
        <insert necessary documentation here>
        '''
        if self.denoise_fit[0] > self.denoise_fit[5]:
            return input.idxmin(), input.min()
        else:
            return input.idxmax(), input.max()
