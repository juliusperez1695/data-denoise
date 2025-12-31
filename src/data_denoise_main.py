'''
<insert necessary documentation here>
'''

from user_interface import DataDenoiseUI

############################################
#~Data Denoise MAIN - Runs the application~#
############################################
def main():

    # Initialize and run the program's user interface
    denoise_ui = DataDenoiseUI()
    prog_ui = denoise_ui.initialize()
    denoise_ui.run_application(prog_ui)

if __name__ == "__main__":
    main()
