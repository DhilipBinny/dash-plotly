import dash
from datetime import datetime as dt
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

sample_datasets = {
    "diamonds" : "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv",
    "anscombe":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/anscombe.csv",
    "attention":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/attention.csv",
    "brain_networks":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/brain_networks.csv",
    "car_crashes":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv",
    "dots":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/dots.csv",
    "exercise":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/exercise.csv",
    "flights":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv",
    "fmri":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/fmri.csv",
    "gammas":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/gammas.csv",
    "iris":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
    "mpg":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv",
    "planets":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv",
    "tips":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv",
    "titanic":"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
}

DF = pd.DataFrame()
PROJECTS  = [ dataset  for dataset, link in sample_datasets.items() ]
PROJECT = "iris"

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

