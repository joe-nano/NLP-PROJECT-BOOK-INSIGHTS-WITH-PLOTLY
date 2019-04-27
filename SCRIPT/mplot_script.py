# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 20:52:08 2019

@author: kennedy
"""

import pandas as pd
import dash
import os 
import nltk
import json
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import plotly.graph_objs as go
from datetime import datetime
from os.path import join
from nltk.tokenize import word_tokenize
french_tok = nltk.data.load('tokenizers/punkt/french.pickle')
from flask import Flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server = server)

#%% data

#get file path
path = '/home/kenneth/Documents/GIT_PROJECTS/NLP-PROJECT-BOOK-INSIGHTS-WITH-PLOTLY'
direc = join(path, 'DATASET/')
data = pd.read_csv(direc + 'collatedsources_v1.csv', sep = ';')
data.set_index(['ID'], inplace = True)
columns = [x for x in data.columns]

#-------------------------------

book_path = join(path, 'DATASET/Collated books v1/')
dirlis = sorted(os.listdir(book_path))[1:]

#%%
#import gensim
#from gensim.utils import simple_preprocess
#from gensim.parsing.preprocessing import STOPWORDS
#from nltk.stem import WordNetLemmatizer, SnowballStemmer
#from nltk.stem.porter import *
#import numpy as np
#import nltk
#nltk.download('wordnet')


#from nltk.stem.snowball import FrenchStemmer
#stemmer = FrenchStemmer()
#stemmer = SnowballStemmer("english")
#stemmer.stem(sample)

#import spacy
#import fr_core_news_sm
#nlp = fr_core_news_sm.load()
#stac = nlp(sample)
#%% app

app.layout = html.Div([
    html.Div([
        #--header section
        html.Div([
                html.H1('Digital Book Insight'),
                ], style={'text-align': 'left','width': '49%', 'display': 'inline-block','vertical-align': 'middle'}),
        html.Div([
                html.H4('Project by Miloskrissak'),
                html.Label('NLP with python 3: Topic visualization in intereative chart. Cluster analysis of word corpus using Naive Bayes algorithm. Hover over the data points to see '+
                           'meta data info the respective books.')
                ], style= {'width': '49%', 'display': 'inline-block','vertical-align': 'middle', 'font-size': '12px'})
                ], style={'background-color': 'white', 'box-shadow': 'black 0px 1px 0px 0px'}),
    #--scaling section
    html.Div([
            #--- x-axis
            html.Div([
                    html.Label('x-scale:'),                    
                    dcc.RadioItems(
                            #---
                            id='x-items',
                            options =[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value = "Linear",
                            labelStyle={'display': 'inline-block'}
                            ), 
                    ], style = {'display': 'inline-block', 'width': '25%'}),
            #--- y-axis
            html.Div([
                    html.Label('y-scale:'),                    
                    dcc.RadioItems(
                            #---
                            id='y-items',
                            options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value = "Linear",
                            labelStyle={'display': 'inline-block'}
                            ), 
                    ], style = {'display': 'inline-block', 'width': '25%'}),
            #--- X-Vals
            html.Div([
                    html.Label('X-Vals:'),                    
                    dcc.RadioItems(
                            #---
                            id='x-vals',
                            options = [{'label': i, 'value': i} for i in ['Views', 'Duration']],
                            value = "Views",
                            labelStyle={'display': 'inline-block'}
                            ), 
                    ], style = {'display': 'inline-block', 'width': '25%'}),
            #--- Sort Tags
            html.Div([
                    html.Label('Sort Tags'),                    
                    dcc.RadioItems(
                            #---
                            id='Sort-Tags',
                            options = [{'label': i, 'value': i} for i in ['A-z', 'Most Tags']],
                            value = "A-z",
                            labelStyle={'display': 'inline-block'}
                            ), 
                    ], style = {'display': 'inline-block', 'width': '25%'})
            ], style={'background-color': 'rgb(204, 230, 244)', 'padding': '1rem 0px', 'margin-top': '2px','box-shadow': 'black 0px 0px 1px 0px'}),
    #-- Graphs
    html.Div([
            #--scatterplot
            #visibility: visible; left: 0%; width: 100%
            html.Div([
                    dcc.Graph(id = 'scatter_plot'),
                    ], style = {'display': 'inline-block', 'width': '65%'}),
            #--horizontal dynamic barplot
            html.Div([
                    dcc.Graph(id = 'bar_plot')
                    ], style = {'display': 'inline-block', 'width': '35%'}),
            ]),
    html.Div([
            dcc.RangeSlider(
                    id='year-slider',
                    min=data.year_edited.min(),
                    max=data.year_edited.max(),
                    value = [data.year_edited.min(), data.year_edited.max()],
                    marks={str(year): str(year) for year in range(data.year_edited.min(), data.year_edited.max(), 5)}
                )
            ], style = {'background-color': 'rgb(204, 230, 244)', 'visibility': 'visible', 'left': '0%', 'width': '49%', 'padding': '0px 20px 20px 20px'}),
    #-- Footer section
    html.Div([
        #--footer section
        html.Div([
                html.Div([
                        html.H2(id = 'topic')], style = {'color':' rgb(35, 87, 137)'}),
                html.Div([
                        html.Label(id = 'date')], style = {'color':' black', 'font-weight': 'bold', 'display': 'inline-block'}),
                html.Div([
                        html.Label(id = 'author')], style = {'color':' black', 'font-weight': 'bold', 'display': 'inline-block', 'padding': '0px 0px 10px 35px'}),
                html.Div([
                        html.Label(id = 'cat')], style = {'color':' black', 'font-weight': 'bold', 'display': 'inline-block', 'padding': '0px 0px 10px 35px'}),
                html.Label(id = 'label'),
                ], style= {'width': '74%', 'display': 'inline-block','vertical-align': 'middle', 'font-size': '12px, '}),
        html.Div([
                html.H2('Topics'),
                html.Label('Dash is a web application framework that provides pure Python')
                ], style={'text-align': 'center','width': '25%', 'display': 'inline-block','vertical-align': 'middle'}),
                ], style={'background-color': 'rgb(204, 230, 244)', 'margin': 'auto', 'width': '100%', 'max-width': '1200px', 'box-sizing': 'border-box', 'height': '30vh'}),
    #---
    #main div ends here
    ],style = {'background-color': 'rgb(204, 230, 244)','margin': 'auto', 'width': '100%', 'display': 'block'})

#--
@app.callback(
        Output('scatter_plot', 'figure'),
        [Input('year-slider', 'value'),
         Input('x-items', 'value'),
         Input('y-items', 'value')])
def update_figure(make_selection, xaxis, yaxis):

    data_places = data[(data.year_edited >= make_selection[0]) & (data.year_edited <= make_selection[1])]
    traces = go.Scatter(
            x = data_places.index,
            y = data_places['book_number'],
            text = [(x, y, z, w, q) for (x, y, z, w, q) in zip(data_places['book_code'], data_places['place'],\
                    data_places['author'], data_places['book_title'] , data_places['year_edited'])],
            mode = 'markers',
            opacity = 0.5,
            marker = {'size': 15, 
                      'opacity': 0.5,
                      'line': {'width': 0.5, 'color': 'white'}},
            )
    
    return {'data': [traces],
            'layout': go.Layout(
                    xaxis={'type': 'linear' if xaxis == 'Linear' else 'log', 'title': 'Book ID'},
                    yaxis={'type': 'linear' if yaxis == 'Linear' else 'log','title': 'Book number'},
                    
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest')
                    }

@app.callback(
        Output('topic', 'children'),
        [Input('scatter_plot', 'hoverData')]
        )
def update_bookheader(hoverData):

    book_number = str(hoverData['points'][0]['text'])[2:7]
    book_path = join(path, 'DATASET/Collated books v1/')
    dirlis = sorted(os.listdir(book_path))[1:]
    for ii in dirlis:
        if ii.strip('.txt') == book_number:
            subject = data[data.book_code == ii.strip('.txt')]['book_title'].values[0]
    return subject

@app.callback(
        Output('date', 'children'),
        [Input('scatter_plot', 'hoverData')]
        )
def update_bookyear(hoverData):
    
    book_number = str(hoverData['points'][0]['text'])[2:7]
    book_path = join(path, 'DATASET/Collated books v1/')
    dirlis = sorted(os.listdir(book_path))[1:]
    for ii in dirlis:
        if ii.strip('.txt') == book_number:
            date = data[data.book_code == ii.strip('.txt')]['year_edited'].values[0]
    return str('YEAR EDITED: ')+ str(date)

@app.callback(
        Output('author', 'children'),
        [Input('scatter_plot', 'hoverData')]
        )
def update_bookauthor(hoverData):
    
    book_number = str(hoverData['points'][0]['text'])[2:7]
    book_path = join(path, 'DATASET/Collated books v1/')
    dirlis = sorted(os.listdir(book_path))[1:]
    for ii in dirlis:
        if ii.strip('.txt') == book_number:
            author = data[data.book_code == ii.strip('.txt')]['author'].values[0]
    return str('Author: ') + author

@app.callback(
        Output('cat', 'children'),
        [Input('scatter_plot', 'hoverData')]
        )
def update_cat(hoverData):
    
    book_number = str(hoverData['points'][0]['text'])[2:7]
    book_path = join(path, 'DATASET/Collated books v1/')
    dirlis = sorted(os.listdir(book_path))[1:]
    for ii in dirlis:
        if ii.strip('.txt') == book_number:
            author = data[data.book_code == ii.strip('.txt')]['book_category_name'].values[0]
    return str('Category: ') + author
    
@app.callback(
        Output('label', 'children'),
        [Input('scatter_plot', 'hoverData')]
        )
def update_label(hoverData):
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    #getting a Nonetype error here
    book_number = str(hoverData['points'][0]['text'])[2:7]
    book_path = join(path, 'DATASET/Collated books v1/')
    dirlis = sorted(os.listdir(book_path))[1:]
    for ii in dirlis:
        if ii.strip('.txt') == book_number:
            with open(book_path + ii, 'rU') as f:
                text = f.read().strip()[0:500]
                text = tokenizer.tokenize(text)
                text = ' '.join(text)
                f.close()
    return text


if __name__ == '__main__':
  app.run_server(debug = True)






