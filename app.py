from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource
import json
import requests
import numpy as np
import pandas as pd

app = Flask(__name__)

app.vars={}

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/graph',methods=['POST'])
def graph():
    try: app.vars['open'] = request.form['opening']
    except: app.vars['open'] = ''
    try: app.vars['close'] = request.form['closing']
    except: app.vars['close'] = ''
    try: app.vars['adj_close'] = request.form['adj_close']
    except: app.vars['adj_close'] = ''
    # f = open('stock.txt', 'w')
    # f.write('Stock: %s\n'%(stock))
    # f.write('Checked: %s\n\n'%(app.vars))
    # f.close()

    symbol=request.form['stock_name']

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

    output_file('stockPlot.html')

    p1 = figure(x_axis_type='datetime', title = 'Stock 2020: '+symbol,
                x_axis_label = 'date', y_axis_label = 'price')
    p1.title.text_font_size = '15pt'
    p1.title.align = 'center'
    if app.vars['open']:
        p1.line(x,op,legend_label="open",line_color='blue')
    if app.vars['close']:
        p1.line(x,cl,legend_label='close',line_color='red')
    if app.vars['adj_close']:
        p1.line(x,adj_cl,legend_label='adj close',line_color='green')

    show(p1)

    return render_template('graph.html')

#@app.route('/graph',methods=['POST'])
#def graph():
#    return render_template('graph.html')

if __name__ == '__main__':
    #app.run(port=33507)
    app.run(debug=True)
