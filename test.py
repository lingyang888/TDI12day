from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource
import json
import requests
import numpy as np
import pandas as pd

symbol='GOOG'

api_key='XPHT5FFL8U5Q53PN'
function = 'TIME_SERIES_DAILY_ADJUSTED'

url='https://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + api_key

stock = requests.get(url).json()
df = pd.DataFrame(stock['Time Series (Daily)'])
df = df.T

a = list(df.index)
end=a.index('2020-05-01')+1
start=a.index('2020-06-01')
x = a[start:end]

x = pd.to_datetime(x)

op = df['1. open'][start:end]
op = op.astype(float)

cl = df['4. close'][start:end]
cl = cl.astype(float)

adj_cl = df['5. adjusted close'][start:end]
adj_cl = adj_cl.astype(float)

output_file('testPlot.html')

p1 = figure(x_axis_type='datetime', title = 'Stock 2020: '+symbol,
            x_axis_label = 'date', y_axis_label = 'price')
p1.title.text_font_size = '15pt'
p1.title.align = 'center'
p1.line(x,op,legend_label="open",line_color='blue')
p1.line(x,cl,legend_label='close',line_color='red')
p1.line(x,adj_cl,legend_label='adj close',line_color='green')

show(p1)
