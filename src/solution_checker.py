'''
<insert necessary documentation here>
'''

class SolutionChecker:
    '''
    <insert necessary documentation here>
    '''
    def __init__(self, data, denoise_data):
        self.orig_fit = data
        self.denoise_fit = denoise_data

    def find_extrema(self, data):
        '''
        <insert necessary documentation here>
        '''
        if self.denoise_fit[0] > self.denoise_fit[5]:
            extr_idx = data.idxmin()
            extr = data.min()
        else:
            extr_idx = data.idxmax()
            extr = data.max()
        return extr_idx, extr
