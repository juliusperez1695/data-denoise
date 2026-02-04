'''
v0.1.0
'''

from user_interface import DataDenoiseCLI

############################################
#~Data Denoise MAIN - Runs the application~#
############################################
def main():
    '''
    <insert helpful documentation here>
    '''
    # Initialize and run the program's user interface
    denoise_ui = DataDenoiseCLI()
    prog_ui = denoise_ui.initialize()
    denoise_ui.run_application(prog_ui)

if __name__ == "__main__":
    main()
