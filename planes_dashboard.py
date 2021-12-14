#%%
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import json
#%%
#data = pd.read_csv('crashes_to_visualize.csv') #Jupyter
data = pd.read_csv(r'Visualisering\Vis_project\crashes_to_visualize.csv') #Dash
data = data.drop(data.columns[0], axis=1)

#%%
#data["total_passengers_dead"].astype(int)
long = data["Crash_location_city_longitude"]

lat = data["Crash_location_city_latitude"]
#%%
app = dash.Dash(__name__)

mintime = data['Year'].min()
maxtime = data['Year'].max()


types = data['Organisation'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'All organisations', 'value': 'all'})

app.layout =html.Div([
                html.H1(children="The World's Plane Crashes",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),    
                html.Div([
                        html.Div([
                            dcc.Dropdown(
                            id='organisation',
                            options=type_options,
                            value='all',
                            #multi = True,
                            style={'width':'50%','display':'inline-block'}),
                         dcc.Graph(id='crash-map'),
                         dcc.RangeSlider(
                            id='time-slider',
                            min=mintime,
                            max=maxtime,
                            step=1,
                            value=[mintime,maxtime],
                            tooltip={"placement": "bottom", "always_visible": True}),
                        dcc.Graph(id='pie_chart')
                    ],style={'width':'62%','display':'inline-block','vertical-align':'top','margin':'2%'})
                     ]),
                 ])
    
@app.callback(Output('pie_chart','figure'),
    [
        Input('crash-map','clickData'),        
    ])
def click_updater(click_data):
    if click_data != None:

        custom_data = click_data['points'][0]['customdata']
        custom_data
        fig_2 = px.pie(data_frame=click_data, 
                values=[custom_data[6],custom_data[7],custom_data[8],custom_data[9],custom_data[10]], 
                names=['Dead passengers','Dead crew','Surviving passengers','Surviving crew','People killed on ground'],
                title='DEAD')
    return fig_2


@app.callback(
    Output(component_id='crash-map', component_property='figure'),
    #Output(component_id='pie_chart', component_property='figure'),
    [
        Input(component_id='time-slider', component_property='value'),
        Input(component_id='organisation', component_property='value'),
        #Input(component_id='crash-map',component_property='clickData'),        
    ]
)

def update_output(time, organisation):
    mydata = data
    if organisation != 'all':
       mydata = data[data['Organisation'] == organisation]
    if time != [mintime,maxtime]:
        mydata = mydata[mydata['Year'] >= time[0]]
        mydata = mydata[mydata['Year'] <= time[1]]
    fig_1 = px.scatter_mapbox(data_frame=mydata, 
                        lat="Crash_location_city_longitude",
                        lon="Crash_location_city_latitude",
                        hover_data=["Organisation",
                                    "Crash_location_country",
                                    "Crash_location_city",
                                    "Date",
                                    "Year",
                                    "Ac_type",
                                    'Passengers dead',
                                    'Crew dead',
                                    'Passengers survivors',
                                    'Crew survivors',
                                    'Ground_fatalities_num'],
                        color='Total dead',
                        color_continuous_scale='magma',
                        size=[max(10, i) for i in mydata['Total dead']],
                        size_max=30,
                        zoom=1,
                        width = 1200,
                        height=800)
    #print("plotly express hovertemplate:", fig_1.data[0].hovertemplate)
    fig_1.update_traces(hovertemplate = "<br>Organisation: %{customdata[0]}<br>Country/State: %{customdata[1]}<br>City: %{customdata[2]}<br>Date: %{customdata[3]} %{customdata[4]}<br>Aircraft type: %{customdata[5]}<extra></extra>")
    fig_1.update_layout(mapbox_style='carto-positron', autosize=False)
    fig_1.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    
    return fig_1

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)