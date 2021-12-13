#%%
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
#%%

data = pd.read_csv(r'Visualisering\Vis_project\trimmed_crashes_city5k.csv')
data = data.drop(data.columns[0], axis=1)

# %%
#%%
app = dash.Dash(__name__)
"""
types = data['Organisation'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'All Volcano Types', 'value': 'all'})

rocks = data['major_rock_1'].unique()
rock_options = [{'label': i, 'value': i} for i in rocks]
rock_options.append({'label': 'All Rock Types', 'value': 'all'})

# mintime = data['last_eruption_year'].min()
# maxtime = data['last_eruption_year'].max()
mintime = 1900
maxtime = 2030
"""
app.layout =    html.Div([
                     html.Div([
                         dcc.Graph(id='crash-map')
                     ],style={'width':'46%','display':'inline-block','vertical-align':'top','margin':'2%'}),
                     html.Div([
                         html.Div(id='miframe')
                     ],style={'width':'46%','display':'inline-block','vertical-align':'top','margin':'2%'})
                 ]),
                html.Div([
                     dcc.RangeSlider(
                       id='time-slider',
                       min=mintime,
                       max=maxtime,
                       step=100,
                       value=[mintime,maxtime],
                       marks={i: str(i) for i in range(mintime, maxtime, 500)})
                 ])


@app.callback(
    Output(component_id='crash-map', component_property='figure'),
    [
        #Input(component_id='volcano_types', component_property='value'),
        #Input(component_id='volcano_rocks', component_property='value'),
        #Input(component_id='time-slider', component_property='value')
    ]
)
def update_output(volcano_type, volcano_rock, time):
    mydata = data
    """
    if volcano_type != 'all':
        mydata = data[data['primary_volcano_type'] == volcano_type]
    if volcano_rock != 'all':
        mydata = mydata[mydata['major_rock_1'] == volcano_rock]
    if time != [mintime,maxtime]:
        mydata = mydata[mydata['last_eruption_year'] >= time[0]]
        mydata = mydata[mydata['last_eruption_year'] <= time[1]]
        """
    fig = px.scatter_mapbox(data_frame=mydata, 
                        lat="Crash_location_city_latitude",
                        lon="Crash_location_city_longitude",
                        hover_name="Flight_num",
                        size=[len(data)],
                        size_max=10,
                        zoom=0,
                        height=1000)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)