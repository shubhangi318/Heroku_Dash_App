import io
import base64
import pandas as pd
import dash_table as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

app = dash.Dash(name=__name__)
server = app.server

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Data', children=[
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False),
    
    html.Br(),
    html.Div([
     html.Div([
         
         html.Div([
            html.Pre(children= "Age Group",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
    dcc.Checklist(
        id='dropdown1',
        options=[],
        value="",
        labelStyle={'display': 'block'},
        style={"height":100, "width":200, "overflow":"auto"})
    ,
    
    html.Div([
       html.Pre(children= "Gender",
       style={"text-align": "center", "font-size":"100%", "color":"black"})
   ]),
    dcc.Checklist(
        id='dropdown2',
        options=[],
        value="",
        labelStyle={'display': 'block'},
        style={"height":100, "width":200, "overflow":"auto"})
    
    ], style={'width': '20%', 'display': 'block'}),
    
    # ]),
    # html.Div([
        
        html.Div([
    dt.DataTable(data=[], id='table')
    
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
    dcc.Graph(id="graph1")
    ], style={'width': '40%', 'display': 'inline-block'})
    
    ], style={'display': 'flex'})
    
    ]),
        
        dcc.Tab(label='Weekly Summary', children=[
            html.Div([
            html.Div([
                
                html.Div([
                   html.Pre(children= "Age Group",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
            dcc.Checklist(
                id='dropdown3',
                options=[],
                value="",
                labelStyle={'display': 'block'},
                style={"height":100, "width":200, "overflow":"auto"}),
            
            html.Div([
               html.Pre(children= "Gender",
               style={"text-align": "center", "font-size":"100%", "color":"black"})
           ]),
            dcc.Checklist(
                id='dropdown4',
                options=[],
                value="",
                labelStyle={'display': 'block'},
                style={"height":100, "width":200, "overflow":"auto"}),
            
            html.Div([
               html.Pre(children= "Week",
               style={"text-align": "center", "font-size":"100%", "color":"black"})
           ]),
            dcc.Dropdown(
                id='dropdown5',
                options=[],
                value="")
            
            
            ],style={'padding-right':'25%'}),

            html.Div([
                html.Div([
                   html.Pre(children= "Weekly Summary",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
                
        dt.DataTable(data=[], id='summary')
        
        ], style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex'})
            
            ]),
        dcc.Tab(label='Weekly Usage', children=[
            html.Div([
            html.Div([
                html.Div([
                   html.Pre(children= "Age Group",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
            dcc.Checklist(
                id='dropdown6',
                options=[],
                value="",
                labelStyle={'display': 'block'},
                style={"height":100, "width":200, "overflow":"auto"}),
            html.Div([
               html.Pre(children= "Gender",
               style={"text-align": "center", "font-size":"100%", "color":"black"})
           ]),
            dcc.Checklist(
                id='dropdown7',
                options=[],
                value="",
                labelStyle={'display': 'block'},
                style={"height":100, "width":200, "overflow":"auto"}),
            html.Div([
               html.Pre(children= "Week",
               style={"text-align": "center", "font-size":"100%", "color":"black"})
           ]),
            dcc.Dropdown(
                id='dropdown8',
                options=[],
                value="")
            
            
            ]),
            
            
            
            html.Div([
                
                html.Div([
                   html.Pre(children= "Weekwise Trendline",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
            dcc.Graph(id="graph2")
            
            ], style={'width': '100%', 'display': 'inline-block'})
          ], style={'display': 'flex'})  
        ]),
        
        dcc.Tab(label='Volume of Business', children=[
            html.Div([
            html.Div([
                
                html.Div([
                   html.Pre(children= "Week",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
            dcc.Dropdown(
                id='dropdown9',
                options=[],
                value="",
                style={"width":200})
            
            
            ]),
            
            html.Div([
                
                html.Div([
                   html.Pre(children= "Customer Average Usage",
                   style={"text-align": "center", "font-size":"100%", "color":"black"})
               ]),
            dcc.Graph(id="graph3")
            ], style={'width': '100%', 'display': 'inline-block'})
            ]  , style={'display': 'flex'})
            
            ])
    ])
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None
    return df



@app.callback(
    [Output("table", "data"), 
     Output("table", "columns")],
    [Input("upload-data", "contents"), 
     Input("upload-data", "filename"),
     Input("dropdown1", "value"),
     Input("dropdown2", "value")])
def update_output(contents, filename,dropdown1,dropdown2):
    if contents is not None:
        df = parse_contents(contents, filename)
        # add some operations/calculations and show results
        if df is not None:
            # df2 = df[(df['Age_Group'] == dropdown1) & (df['Gender'] == dropdown2)]
               
            df2 = df[df['Age_Group'].isin(dropdown1)]
            df2 = df2[df2['Gender'].isin(dropdown2)]
            # df2 = df2.groupby(['Age_Group','Gender'])['CustID'].count().reset_index()
            df3 = df2.groupby('Week').agg(
                Avg_Calls=pd.NamedAgg(column="Calls", aggfunc="mean"),
                Avg_Minutes=pd.NamedAgg(column="Minutes", aggfunc="mean"),
                Avg_Amt=pd.NamedAgg(column="Amt", aggfunc="mean")).reset_index()
            tmp = df3.select_dtypes(include=[np.number])
            df3.loc[:, tmp.columns] = np.round(tmp)
            return df3.to_dict("records"), [{"name": i, "id": i} for i in df3.columns]
        else:
            return [{}], []
    else:
        return [{}], []


@app.callback(
    Output('dropdown1', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Age_Group'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []
    
    
@app.callback(
    Output('dropdown2', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options2(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Gender'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []  


@app.callback(
    Output('dropdown3', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options3(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Age_Group'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []
    
    
@app.callback(
    Output('dropdown4', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options4(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Gender'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []  
    
@app.callback(
    Output('dropdown5', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options5(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Week'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return [] 
    
    

@app.callback(
    Output('dropdown6', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options6(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Age_Group'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []


@app.callback(
    Output('dropdown7', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options7(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df['Gender'].unique()
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []    

 
@app.callback(
    Output('dropdown8', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options8(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df.columns[2:5]
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []
    
    
@app.callback(
    Output('dropdown9', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options9(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        df = df.columns[2:5]
        # lst = [{'label': i, 'value': i} for i in df.columns]
        return df
    else:
        return []
   
@app.callback(
    Output("graph1", "figure"),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'), 
    Input("dropdown1", "value"),
    Input("dropdown2", "value"))
def update_bar_chart(contents, filename,dropdown1,dropdown2):
    if contents is not None:
        df = parse_contents(contents, filename)
        # add some operations/calculations and show results
        if df is not None:
            df2 = df[df['Age_Group'].isin(dropdown1)]
            df2 = df2[df2['Gender'].isin(dropdown2)]
            df3 = df2['Active'].value_counts().reset_index()

            fig = px.pie(df3, values='Active', names='index', title='Pie Chart')
    return fig


@app.callback(
    [Output("summary", "data"), 
     Output("summary", "columns")],
    [Input("upload-data", "contents"), 
     Input("upload-data", "filename"),
     Input("dropdown3", "value"),
     Input("dropdown4", "value"),
     Input("dropdown5", "value")],
)
def update_output2(contents, filename,dropdown3,dropdown4,dropdown5):
    if contents is not None:
        df = parse_contents(contents, filename)
        # add some operations/calculations and show results
        if df is not None:
            # df2 = df[(df['Age_Group'] == dropdown1) & (df['Gender'] == dropdown2)]
               
            df2 = df[df['Age_Group'].isin(dropdown3)]
            df2 = df2[df2['Gender'].isin(dropdown4)]
            # df2 = df2[df2['Week'].isin(dropdown5)]
            
            df2 = df2[df2["Week"] == dropdown5]
            # df2 = df2.groupby(['Age_Group','Gender'])['CustID'].count().reset_index()
            df3 = df2.describe().reset_index()
            tmp = df3.select_dtypes(include=[np.number])
            df3.loc[:, tmp.columns] = np.round(tmp)
            
            return df3.to_dict("records"), [{"name": i, "id": i} for i in df3.columns]
        else:
            return [{}], []
    else:
        return [{}], []   


@app.callback(
    Output("graph2", "figure"),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'), 
    Input("dropdown6", "value"),
    Input("dropdown7", "value"),
    Input("dropdown8", "value"))
def update_bar_chart2(contents, filename,dropdown6,dropdown7,dropdown8):
    if contents is not None:
        df = parse_contents(contents, filename)
        # add some operations/calculations and show results
        if df is not None:
            df2 = df[df['Age_Group'].isin(dropdown6)]
            df2 = df2[df2['Gender'].isin(dropdown7)]
            
            df3 = df2.groupby('Week').agg(
                Calls=pd.NamedAgg(column="Calls", aggfunc="mean"),
                Minutes=pd.NamedAgg(column="Minutes", aggfunc="mean"),
                Amt=pd.NamedAgg(column="Amt", aggfunc="mean")).reset_index()
            
            # df4 = df3[dropdown8]
            
            fig = px.line(df3,x="Week", y=dropdown8,markers=True)
    return fig


@app.callback(
    Output("graph3", "figure"),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'), 
    Input("dropdown9", "value"))
def update_bar_chart3(contents, filename,dropdown9):
    if contents is not None:
        df = parse_contents(contents, filename)
        # add some operations/calculations and show results
        if df is not None:
            
            df3 = df.groupby(['Age_Group','Gender']).agg(
                Calls=pd.NamedAgg(column="Calls", aggfunc="mean"),
                Minutes=pd.NamedAgg(column="Minutes", aggfunc="mean"),
                Amt=pd.NamedAgg(column="Amt", aggfunc="mean")).reset_index()
            
            fig = px.bar(df3, x="Age_Group", y=dropdown9, 
                 color="Gender", barmode="group")
            
    return fig


if __name__ == '__main__':
    app.run_server()