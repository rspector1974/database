#from jupyter_plotly_dash import JupyterDash
import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State
import base64 
import os
import numpy as np
import plotly.express as px
from jupyter_dash import JupyterDash

from pymongo import MongoClient
from bson.json_util import dumps

# Import crud fucntions from project1.py file
from  dbenhancecrudmethods import AnimalShelter





###########################
# Data Manipulation / Model
###########################
# set mongodb username and password
username = "admin"
password = "root"
shelter = AnimalShelter(username, password) # pass username and password to login method


# class read method must support return of cursor object 
df = pd.DataFrame.from_dict(shelter.read({})) #read in data from read method in crud class


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

image_filename = 'GSLogo.png' # logo file name variable
encoded_image = base64.b64encode(open(image_filename, 'rb').read()) #use base64 to encode logo file

#define dash layout

app.layout = html.Div([
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))), #logo inclusion
    html.Center(html.H1('Robin Spector''s CS-340 Final Project 2 Updated for ePortfolio ')), #Unique ID for project
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    #create radio button filters
    html.Div( dcc.RadioItems(
        id='filter-type',
       options=[
           {'label': 'Animal Type', 'value': 'animal_type'},
           {'label': 'Breed', 'value': 'breed'},
           {'label': 'Age','value': 'age_upon_outcome'},
           {'label': 'Color','value': 'color'},
           {'label': 'Name','value':'name'},
           {'label': 'Reset View','value':'reset_view'}
       ],
    
            labelStyle ={'display': 'inline-block'},
           ),
            ),
            
     
     html.Div([
                html.Label('Search Database'),
                dcc.Input(id='input-on-submit', type='text', placeholder='Select Category/Enter Term'),
                html.Br(),
                html.Br(),html.Br(),
                html.Button('Submit', id='btn-submit',n_clicks=0),
                
                
            ]),
   html.Hr(),
    #define datatable format
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable= False, # table is not editable
        filter_action="native", # use the native filtering method
        sort_action="native", # use the native sort method
        sort_mode="multi", # all sorting by multile columns
        page_action="native", # native page action
        page_current=0, # start with the first page
        page_size=10,

    ),
    html.Br(),
    html.Hr(),
    html.Center(html.H1("Please Choose Graph Output Value Option")),
    
    
#Graph Drop Down Menu
    
    html.Div(dcc.Dropdown(
        id='filter-type_graph',
       options=[
           {'label': 'Animal Type', 'value': 'animal_type'},
           {'label': 'Breed', 'value': 'breed'},
           {'label': 'Age','value': 'age_upon_outcome'},
           {'label': 'Color','value': 'color'},
           {'label': 'Name','value':'name'},
           {'label': 'Do Not Display Chart','value':'no_chart'}
        
       ],
         value = 'no_chart' # Default Setting
          ),
            ),
   
  #Formatting for graph and map position  
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################
# call back for filtering functionality
@app.callback([Output('datatable-id','data'),
             Output('datatable-id','columns')],
             [Input('filter-type','value'),
              Input('btn-submit','n_clicks')],
             [State('input-on-submit', 'value')])
#DB queries based on filtering option
def update_dashboard(radio_button,clicked,input1):
    df = pd.DataFrame.from_records(shelter.read({}))
   # Logic for database query. If search term is selected catagory, wild card search using regex
    if radio_button == "animal_type" and input1 and clicked:
        df = pd.DataFrame(list(shelter.read({"animal_type":{"$regex": input1,"$options" :'i' }})))
    elif radio_button == "breed" and input1 and clicked:
        df = pd.DataFrame(list(shelter.read({"breed":{"$regex": input1,"$options" :'i' }})))
    elif radio_button == "age_upon_outcome" and clicked:
        df = pd.DataFrame(list(shelter.read({"age_upon_outcome":{"$regex": input1,"$options" :'i' }})))
    elif radio_button == "color" and input1 and clicked:
        df = pd.DataFrame(list(shelter.read({"color":{"$regex": input1,"$options" :'i' }})))
    elif radio_button == "name" and input1 and  clicked:
        df = pd.DataFrame(list(shelter.read({"name":{"$regex": input1,"$options" :'i' }})))
        
    if radio_button == "reset_view":
        df = pd.DataFrame.from_records(shelter.read({}))
  
        
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    
    return (data,columns)



# call back for Graph
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
    Input('filter-type_graph','value')])
def update_graphs(viewData,radio_button):
    dff = pd.DataFrame.from_dict(viewData)
    chart_values = radio_button
    #Pie chart code
    if chart_values == "no_chart":
        return ""
    elif chart_values :
        return [
            dcc.Graph(            
            figure = px.pie(dff, names = chart_values)
            )    
        ]
 # Call back for map
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id','active_cell'),
     Input('datatable-id', 'derived_viewport_data')])

def update_map(activeCell,viewData):
#Geolocation Code
    dfff = pd.DataFrame.from_records(viewData)
    if activeCell is not None: # if a cell is selected
           row = activeCell['row'] #return the row # to row variable
    else: # if cell is not selected default to row 0
            row = 0    
    # set center,and marker to location_lat, and location_long from data table.    
    return [
            dl.Map(style={'width': '1000px', 'height': '500px'}, center=[dfff.loc[row,'location_lat'],dfff.loc[row,'location_long']], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
                dl.Marker(position=[dfff.loc[row,'location_lat'],dfff.loc[row,'location_long']], children=[
                    dl.Tooltip(dfff.loc[row,'breed']), # return breed as a tool tip based on row location
                    dl.Popup([
                        html.H1("Animal Name"),
                        html.P(dfff.loc[row,'name']) # return animal name as a pop up based on row location
                    
                    ])
                ])
            ])
        ]    
        
        
        
        

 


app.run_server(mode='inline')