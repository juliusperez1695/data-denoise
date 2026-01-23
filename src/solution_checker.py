'''
<insert helpful documentation here>
'''
import math
import pandas as pd

class SolutionChecker:
    '''
    <insert helpful documentation here>
    '''
    def __init__(self, init_params, deno_params, fit_mode):
        self.init_params = init_params
        self.deno_params = deno_params
        self.fit_mode = fit_mode

    def run_comparison(self) -> pd.DataFrame:
        '''
        <insert helpful documentation here>
        '''
        if self.fit_mode == 1:
            results = self.report_parabola_results()
        elif self.fit_mode == 2:
            results = self.report_sigmoid_results()
        elif self.fit_mode == 3:
            results = self.report_linear_results()
        elif self.fit_mode == 4:
            results = self.report_exponential_results()
        else:
            results = self.report_parabola_results()

        return results

    def report_parabola_results(self) -> pd.DataFrame:
        '''
        Docstring for report_parabola_results

        :return: Description
        :rtype: DataFrame
        '''
        print("RESULTS: Parabolic Data")
        print("Extreme Loc - Max/Min Location along the independent axis")
        print("Extreme Value - Max/Min value along dependent axis")

        init_a = self.init_params[0]
        init_b = self.init_params[1]
        init_c = self.init_params[2]

        deno_a = self.deno_params[0]
        deno_b = self.deno_params[1]
        deno_c = self.deno_params[2]

        report = pd.DataFrame(columns = ["Extreme Loc", "Extreme Value"],
                              index = ["Initial Fit", "Denoise Fit"])

        init_extr_loc = -1*init_b / (2*init_c)
        deno_extr_loc = -1*deno_b / (2*deno_c)
        report.at["Initial Fit", "Extreme Loc"] = init_extr_loc
        report.at["Denoise Fit", "Extreme Loc"] = deno_extr_loc

        init_extr_val = init_a + init_b*init_extr_loc + init_c*init_extr_loc**2
        deno_extr_val = deno_a + deno_b*deno_extr_loc + deno_c*deno_extr_loc**2
        report.at["Initial Fit", "Extreme Value"] = init_extr_val
        report.at["Denoise Fit", "Extreme Value"] = deno_extr_val

        return report

    def report_sigmoid_results(self) -> pd.DataFrame:
        '''
        Docstring for report_sigmoid_results

        :return: Description
        :rtype: DataFrame
        '''
        print("RESULTS: Sigmoidal Data")
        print("High Level - average value beyond the transition ('ON' state)")
        print("Low Level - average value below the transition ('OFF' state)")
        print("Transition Point - location of transition along independent axis")
        print("Transition Rate - rate at which the transition occurs")

        init_a = self.init_params[0]
        init_b = self.init_params[1]
        init_c = self.init_params[2]
        init_d = self.init_params[3]

        deno_a = self.deno_params[0]
        deno_b = self.deno_params[1]
        deno_c = self.deno_params[2]
        deno_d = self.deno_params[3]

        report = pd.DataFrame(columns = ["High Level",
                                         "Low Level",
                                         "Transition Point",
                                         "Trans. Rate"],
                              index = ["Initial Fit", "Denoise Fit"])

        report.at["Initial Fit", "High Level"] = init_a + init_d # a + d
        report.at["Denoise Fit", "High Level"] = deno_a + deno_d

        report.at["Initial Fit", "Low Level"] = init_d # d
        report.at["Denoise Fit", "Low Level"] = deno_d

        report.at["Initial Fit", "Transition Point"] = init_c # c
        report.at["Denoise Fit", "Transition Point"] = deno_c

        report.at["Initial Fit", "Trans. Rate"] = 0.25 * init_a * init_b # rate = 1/4 * a * b
        report.at["Denoise Fit", "Trans. Rate"] = 0.25 * deno_a * deno_b

        return report

    def report_linear_results(self) -> pd.DataFrame:
        '''
        Docstring for report_linear_results

        :return: Description
        :rtype: DataFrame
        '''
        print("RESULTS: Linear Data")
        print("Slope - rate of increase/decrease")
        print("Intercept - intersection point along dependent axis")

        init_a = self.init_params[0]
        init_b = self.init_params[1]

        deno_a = self.deno_params[0]
        deno_b = self.deno_params[1]

        report = pd.DataFrame(columns = ["Slope", "Intercept"],
                              index = ["Initial Fit", "Denoise Fit"])

        report.at["Initial Fit", "Slope"] = init_a
        report.at["Denoise Fit", "Slope"] = deno_a

        report.at["Initial Fit", "Intercept"] = init_b
        report.at["Denoise Fit", "Intercept"] = deno_b

        return report

    def report_exponential_results(self) -> pd.DataFrame:
        '''
        Docstring for report_exponential_results

        :return: Description
        :rtype: DataFrame
        '''
        print("\n\nRESULTS: Exponential Data")
        print("Intercept - intersection point along dependent axis")
        print("Time Const (tau) - inverse of exponent coefficient, '+/-inf' for unstable growth")
        print("Steady-state value - occurs at 5*tau, '+/-inf' for unstable growth")

        init_a = self.init_params[0]
        init_b = self.init_params[1]
        init_c = self.init_params[2]
        init_d = self.init_params[3]

        deno_a = self.deno_params[0]
        deno_b = self.deno_params[1]
        deno_c = self.deno_params[2]
        deno_d = self.deno_params[3]

        report = pd.DataFrame(columns = ["Intercept",
                                         "Time Constant",
                                         "Steady-state"],
                              index = ["Initial Fit", "Denoise Fit"])

        # Report Intercept
        report.at["Initial Fit", "Intercept"] = init_a*math.exp(init_b*-1*init_c) + init_d
        report.at["Denoise Fit", "Intercept"] = deno_a*math.exp(deno_b*-1*deno_c) + deno_d

        # Report Time Constant
        if init_b < 0:
            init_tau = 1 / init_b
            deno_tau = 1 / deno_b
        elif init_a < 0:
            init_tau = -math.inf
            deno_tau = -math.inf
        else:
            init_tau = math.inf
            deno_tau = math.inf
        report.at["Initial Fit", "Time Constant"] = init_tau
        report.at["Denoise Fit", "Time Constant"] = deno_tau

        # Report Steady-state value
        if init_b < 0:
            init_ss = init_a*math.exp(init_b*(init_tau-init_c)) + init_d
            deno_ss = deno_a*math.exp(deno_b*(deno_tau-deno_c)) + deno_d
        elif init_a < 0:
            init_ss = -math.inf
            deno_ss = -math.inf
        else:
            init_ss = math.inf
            deno_ss = math.inf
        report.at["Initial Fit", "Steady-state"] = init_ss
        report.at["Denoise Fit", "Steady-state"] = deno_ss

        return report

    def build_compare_df(self, initial_df : pd.DataFrame, final_df : pd.DataFrame):
        '''
        Docstring for build_compare_df

        :param self: Description
        :param initial_df: Description
        :type initial_df: pd.DataFrame
        :param final_df: Description
        :type final_df: pd.DataFrame
        '''
        output_df = pd.DataFrame(columns=["x_init", "y_init", "x_final", "y_final"])
        output_df["x_init"] = initial_df[0]
        output_df["y_init"] = initial_df[1]
        output_df["x_final"] = final_df[0]
        output_df["y_final"] = final_df[1]

        return output_df
