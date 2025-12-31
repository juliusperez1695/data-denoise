import os
from data_denoise import DataDenoiser
from time import sleep

class DataDenoiseUI:
    def initialize(self):
        denoiser = DataDenoiser()

        fit_type_menu = Menu("Data Denoise: Choose a Fitting Method\nThis will be used to identify and remove outliers from your dataset.",
                         {
                            '1': {'text':"Parabolic",
                                   'action':denoiser.run_outlier_removal,
                                   'args':(1,)},
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
        prog_menu.run()

class Menu:
    def __init__(self, prompt, options, exit_msg):
        self.prompt = prompt
        self.options = options
        self.exit_msg = exit_msg

    def display(self):
        print("\n\n"+self.prompt)
        for key, value in self.options.items():
            print(f"[{key}]     {value['text']}")

    def get_user_choice(self):
        while True:
            choice = input("\nSelect from the options above: ").upper()

            if choice == 'Q':
                print("\n"+self.exit_msg)
                return choice
            elif choice in self.options and choice != 'Q':
                print("\nRunning \""+self.options[choice]['text']+"\"")
                sleep(1.5)
                return choice
            else:
                print("Invalid input - try again.")
                sleep(1.5)

    def run_user_choice(self, choice):
        args = self.options[choice].get("args", ())
        self.options[choice]['action'](*args)

    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display()
            choice = self.get_user_choice()
            if choice == 'Q':
                break
            else:
                self.run_user_choice(choice)

