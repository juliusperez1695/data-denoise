from DataDenoise import DataDenoiser
from DataProcessor import DataProcessor
from time import sleep

class DataDenoiseUI:
    def Initialize(self):
        denoiser = DataDenoiser()
        dataprocessor = DataProcessor()

        self.fit_type_menu = Menu("Data Denoise: Choose a Fitting Method\nThis will be used to identify and remove outliers from your dataset.",
                         {
                            '1': {'text':"Parabolic",
                                   'action':denoiser.Run_OutlierRemoval,
                                   'args':(1,)},
                            'Q': {'text':"Return to Data Processing Menu",
                                  'action':quit}
                         }, exit_msg="")
        
        self.proc_menu = Menu("Data Denoise: Data Processing Menu",
                         {
                            '1': {'text':"Plot Imported Data",
                                   'action':denoiser.Run_Plotter},
                            '2': {'text':"Handle Outliers",
                                  'action':self.fit_type_menu.Run},
                            '3': {'text':"Check Solution",
                                  'action':denoiser.Run_SolutionCheck},
                            'Q': {'text':"Return to MAIN MENU",
                                  'action':quit}
                         }, exit_msg="")
        
        self.MAIN_MENU = Menu("Welcome!\n\nData Denoise: MAIN MENU",
                         {
                            '1': {'text':"Import Data",
                                   'action':denoiser.importData},
                            '2': {'text':"Process Data",
                                  'action':self.proc_menu.Run},
                            'Q': {'text':"Quit",
                                  'action':quit}
                         }, exit_msg="Program Terminated - Goodbye!")
        
    def RUN(self):
        self.MAIN_MENU.Run()

class Menu:
    def __init__(self, prompt, options, exit_msg):
        self.prompt = prompt
        self.options = options
        self.exit_msg = exit_msg

    def Display(self):
        print("\n"+self.prompt)
        for key, value in self.options.items():
            print(f"[{key}]     {value['text']}")

    def Get_UserChoice(self):
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

    def Run_UserChoice(self, choice):
        args = self.options[choice].get("args", ())
        self.options[choice]['action'](*args)

    def Run(self):
        while True:
            self.Display()
            choice = self.Get_UserChoice()
            if choice == 'Q':
                break
            else:
                self.Run_UserChoice(choice)

