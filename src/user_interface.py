'''
<insert helpful documentation here>
'''
from time import sleep
from data_denoise import DataDenoiser

class DataDenoiseUI:
    '''
    <insert helpful documentation here>
    '''
    def initialize(self):
        '''
        <insert helpful documentation here>
        '''
        denoiser = DataDenoiser()

        fit_type_menu_info = "This will be used to identify and remove outliers from your dataset."
        fit_type_menu = Menu("Data Denoise: Choose a Fitting Method\n"+fit_type_menu_info,
                         {
                            '1': {'text':"Parabolic",
                                   'action':denoiser.run_outlier_removal,
                                   'args':(1,)},
                            '2': {'text':"Sigmoid",
                                   'action':denoiser.run_outlier_removal,
                                   'args':(2,)},
                            '3': {'text':"Linear",
                                   'action':denoiser.run_outlier_removal,
                                   'args':(3,)},
                            '4': {'text':"Exponential",
                                   'action':denoiser.run_outlier_removal,
                                   'args':(4,)},
                            'Q': {'text':"Return to Data Processing Menu",
                                  'action':quit}
                         }, exit_msg="")

        proc_menu = Menu("Data Denoise: Data Processing Menu",
                         {
                            '1': {'text':"Plot Imported Data",
                                   'action':denoiser.run_plotter},
                            '2': {'text':"Handle Outliers",
                                  'action':fit_type_menu.run},
                            '3': {'text':"Check Solution",
                                  'action':denoiser.run_solution_check},
                            'Q': {'text':"Return to MAIN MENU",
                                  'action':quit}
                         }, exit_msg="")

        main_menu = Menu("Data Denoise: MAIN MENU",
                         {
                            '1': {'text':"Import Data",
                                   'action':denoiser.import_data},
                            '2': {'text':"Process Data",
                                  'action':proc_menu.run},
                            'Q': {'text':"Quit",
                                  'action':quit}
                         }, exit_msg="Program Terminated - Goodbye!")

        return main_menu

    def run_application(self, prog_menu):
        '''
        <insert helpful documentation here>
        '''
        prog_menu.run()

class Menu:
    '''
    <insert helpful documentation here>
    '''
    def __init__(self, prompt, options, exit_msg):
        self.prompt = prompt
        self.options = options
        self.exit_msg = exit_msg

    def display(self):
        '''
        <insert helpful documentation here>
        '''
        print("\n\n"+self.prompt)
        for key, value in self.options.items():
            print(f"[{key}]     {value['text']}")

    def get_user_choice(self):
        '''
        <insert helpful documentation here>
        '''
        run_loop = True
        while run_loop:
            choice = input("\nSelect from the options above: ").upper()

            if choice == 'Q':
                print("\n"+self.exit_msg)
                run_loop = False
            elif choice in self.options and choice != 'Q':
                print("\nRunning \""+self.options[choice]['text']+"\"")
                sleep(1.5)
                run_loop = False
            else:
                print("Invalid input - try again.")
                sleep(1.5)
        return choice

    def run_user_choice(self, choice):
        '''
        <insert helpful documentation here>
        '''
        args = self.options[choice].get("args", ())
        self.options[choice]['action'](*args)

    def run(self):
        '''
        <insert helpful documentation here>
        '''
        run_loop = True
        while run_loop:
            # os.system('cls' if os.name == 'nt' else 'clear')
            self.display()
            choice = self.get_user_choice()
            if choice == 'Q':
                run_loop = False
            else:
                self.run_user_choice(choice)
