    
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime 
import sys
import warnings

FILE_NAME = 'Nat_Gas.csv'

class Utilities():

    @staticmethod
    def process_x(x_val) -> int:
        native = int(x_val.timestamp() * 10**9)/1000000000000000
        return native

    # @staticmethod
    # def deprocess_x(x_val: int) -> TimeStamp:
    #     x = (x_val / 10 ** 9) * 1000000000000000
    #     deprocess = datetime.datetime.utcfromtimestamp(x)
    #     return deprocess

    @staticmethod
    def process_x_from_float(x_val: float) -> int:
        native = int(x_val * 10**9)/1000000000000000
        return native

    @staticmethod
    def interp_y_from_x(input : int, x : float, y : float) -> float:
        return np.interp(input, x, y)

    @staticmethod
    def calc_y_fit(x : float,y : float):
        # Add some noise to the data
        y_noise = y + np.random.normal(0, 0.03, x.shape)
        
        # Fit a sine curve to the noisy data with a higher degree polynomial
        p = np.polyfit(x, y_noise, 50)
        y_fit = np.polyval(p, x)
    
        return y_fit

class PredictPrice():

    def __init__(self, dateIn : str):
        self.dateIn = dateIn
        self.fileName = FILE_NAME

    def train_prep_model(self, data):
        # Load the synthetic data
        
        series = data['Prices']
        
        # Fit SARIMA model
        model = SARIMAX(series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit()
        
        # Forecast future values
        forecast = model_fit.forecast(steps=12)
    
        series_new = data['Prices']

        df = pd.DataFrame({'1':series_new,'2':forecast})
    
        # Combine into two lists
        x = []
        y = []
        for a,b in series_new.items():
            # print("process " + str(a))
            native = Utilities.process_x(a)
            x.append(native)
            y.append(b)        
        
        x = np.array(x)
        y = np.array(y)
        return x,y
    
    def runner(self) -> float:
        data = pd.read_csv(self.fileName, index_col='Dates', parse_dates=True)
        x,y = self.train_prep_model(data)
        
        
        y_fit = Utilities.calc_y_fit(x,y)
        # plot_me(x,y, y_fit)
        y = np.array(y_fit)
        
        # y should be sorted for both of these methods
        order = y.argsort()
        y = y[order]
        x = x[order]
    
        prediction = 0.0
        try:
            dt = datetime.datetime.strptime(self.dateIn, "%m/%d/%Y")
            res = dt.timestamp()
            res = Utilities.process_x_from_float(res)
            
            prediction = Utilities.interp_y_from_x(res, x, y)
        except Exception as e:
            print("Error in prediction: " + str(e))
            prediction = 0.0
    
        return float(prediction)