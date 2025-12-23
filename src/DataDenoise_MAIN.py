import os
from UserInterface import *

############################################
#~Data Denoise MAIN - Runs the application~#
############################################
def main():
	
	# Initialize and run the program's user interface
	denoiseUI = DataDenoiseUI()
	prog_UI = denoiseUI.Initialize()
	denoiseUI.RUN(prog_UI)

if __name__ == "__main__":
	main()