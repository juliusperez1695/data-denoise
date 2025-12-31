import os
from user_interface import DataDenoiseUI

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