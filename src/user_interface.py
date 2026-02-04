'''
<insert helpful documentation here>
'''
import json, os
from time import sleep
from data_denoise import DataDenoiser
import plotly.graph_objs as go
import plotly.utils
from plotly.subplots import make_subplots
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import pandas as pd

template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'supersecretkey' # Required for using session
UPLOAD_FOLDER = 'sess_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_plot(df):
    """Generates a Plotly figure and converts it to JSON."""

    if 'indep_var' in df.columns and 'dep_var' in df.columns:#len(df.columns) == 2:
        
        trace1 = go.Scatter(
            x=df['indep_var'].tolist(), 
            y=df['dep_var'].tolist(),
            mode='markers',
            name='Sample Data 1',
                    marker=dict(
                        size=10,
                        color='rgba(199, 10, 165, .9)', # Customize marker color and opacity
                        line=dict(width=1, color='black')
            )
        )

        trace2 = go.Scatter(
            x=df['indep_var'].tolist(), 
            y=df['dep_var'].tolist(),
            mode='markers',
            name='Sample Data 2',
                    marker=dict(
                        size=10,
                        color='rgba(199, 10, 165, .9)', # Customize marker color and opacity
                        line=dict(width=1, color='black')
            )
        )
        
        # fig = go.Figure(data=[trace1])
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Subplot Title 1", "Subplot Title 2"])
        fig.add_trace(trace1, row=1, col=1)
        fig.update_xaxes(title_text="indep_var1", row=1, col=1)
        fig.update_yaxes(title_text="dep_var1", row=1, col=1)
        fig.add_trace(trace2, row=1, col=2)
        fig.update_xaxes(title_text="indep_var2", row=1, col=2)
        fig.update_yaxes(title_text="dep_var2", row=1, col=2)
        fig.update_layout(title_text='Interactive Sub-Plots from CSV Data')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('main_menu.html', message='No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty part
        if file.filename == '':
            return render_template('main_menu.html', message='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session['uploaded_file_path'] = filepath

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(filepath, header=None)
            df.columns = ["indep_var", "dep_var"]

            graphJSON = create_plot(df)

            if graphJSON:
                return render_template('process_menu.html', graphJSON=graphJSON)
            else:
                return render_template('main_menu.html', message='Could not generate plot. Check CSV columns.')
    
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    return render_template('main_menu.html', message='Upload a CSV file to view an interactive plot.')

def run_app(debug_val = False):
    app.run(debug=debug_val)
    
class DataDenoiseCLI:
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
