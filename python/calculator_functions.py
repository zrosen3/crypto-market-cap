import numpy 
import pandas as pd
import plotly.express as px
import io
from flask import Response
import json
import plotly.utils
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#calculate end return of investment
def calculate_return(principal, interest, years, inflation = 0,cap_tax_rate = 0):
    raw_return = principal*(1 + interest/100-inflation/100)**years
    taxes = (raw_return-principal) * cap_tax_rate/100
    tax_adjusted_return = raw_return - taxes
    value_added = tax_adjusted_return - principal
    return [round(tax_adjusted_return, 2), round(taxes, 2), round(value_added, 2)]

#create dataframe of investment over time
def create_df(principal, interest, years, inflation = 0, cap_tax_rate = 0):
    d = {'Year': [int(year) for year in range(0, int(years)+1)]}
    df = pd.DataFrame(data = d)
    df["Value"] = 1.0
    df["Value"] = principal * (1 + interest/100-inflation/100)**df['Year']
    df["Capital gains tax"] = (df["Value"] - principal)* cap_tax_rate/100
    df["Tax adjusted return"] = df["Value"] - df["Capital gains tax"]
    return df


#Test these functions a few times 
#print(calculate_return(100, 10, 10, 1, 1))
df = create_df(100, 10, 30, 1, 1)
df2 = create_df(100, 10, 30, 1, 50)
#print(calculate_return(100, 10, 1, 1, 1))
#print(create_df(100, 10, 1, 1, 1))

#print(calculate_return(100, 10, 1, 1, 1))
#print(create_df(100, 10, 1, 1, 1))

#print(calculate_return(100, 10, 1, 1, 1))
#print(create_df(100, 10, 1, 1, 1))

#print(calculate_return(100, 10, 1, 1, 1))
#print(create_df(100, 10, 1, 1, 1))



