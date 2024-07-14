# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


import plotly.io as pio
pio.renderers.default = 'iframe'



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

df_Launch_Sites = df['Launch Site'].value_counts().reset_index()['Launch Site']
sitesName = [{'label': i, 'value': i} for i in df_Launch_Sites]
sitesName.insert(0, {'label': 'All Sites', 'value': 'ALL'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Record Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
     html.Div([
                   # First inner divsion for  adding dropdown helper text for Selected Drive wheels
                    html.Div([
                            html.H2('Select Site:', style={'margin-right': '2em'}),
                            dcc.Dropdown(id='select_site',
                                options=sitesName,
                                value='ALL',
                                placeholder="Select Site",
                                searchable=True
                            ),
])
         , html.Div([ ], id='plot1'),
          html.Div([
                 dcc.RangeSlider(id='rangeSlider',
                        min=0, max=10000, step=1000,
                        marks={0: '0',
                               1000: '1000',
                               2000: '2000',
                               3000: '3000',
                               4000: '4000',
                               5000: '5000',
                               6000: '6000',
                               7000: '7000',
                               8000: '8000',
                               9000: '9000',
                               10000: '10000'},
                        value=[2000, 5000])
              , html.Div([ ], id='plot2')
         ])
         
     ])
                               ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='plot1', component_property='children'),
               Input(component_id='select_site', component_property='value'),
            )
def showSite(value): 
    if value == "ALL":
      value_counts_sites = data.groupby('Launch Site')['class'].sum().reset_index()
      fig1 = px.pie(value_counts_sites, values='class', names='Launch Site', title="Success ratio of site: {}".format(value)) 
      return [dcc.Graph(figure=fig1)]
    else:
        per_class_value_counts = data[data['Launch Site'] == value].reset_index()['class'].value_counts().reset_index()
        fig1 = px.pie(per_class_value_counts, values='count', names='class', title="Success ratio of site: {}".format(value)) 
        return [dcc.Graph(figure=fig1)]
    return []

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='plot2', component_property='children'),
               [Input(component_id='select_site', component_property='value'), Input(component_id="rangeSlider", component_property="value")],
            )
def showSite(dropdown_value, slider_value): 
    data_in_range = data.loc[(data['Payload Mass (kg)'] >= slider_value[0]) & (data['Payload Mass (kg)'] <= slider_value[1])]
    if dropdown_value == "ALL":
      fig1 = px.scatter(data_in_range, x='Payload Mass (kg)', y='class', color='Booster Version') 
      return [dcc.Graph(figure=fig1)]
    else:
       per_class_value_counts = data_in_range[data_in_range['Launch Site'] == dropdown_value].reset_index()
       fig1 = px.scatter(per_class_value_counts, x='Payload Mass (kg)', y='class', color='Booster Version') 
       return [dcc.Graph(figure=fig1)]
    return []

# Run the app
if __name__ == '__main__':
    app.run_server()
