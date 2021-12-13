#%%
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
#%%

data = pd.read_csv(r'Visualisering\Vis_project\crashes_to_visualize.csv')
data = data.drop(data.columns[0], axis=1)

#%%
#data["total_passengers_dead"].astype(int)
long = data["Crash_location_city_longitude"]

lat = data["Crash_location_city_latitude"]
#%%
app = dash.Dash(__name__)

# mintime = data['last_eruption_year'].min()
# maxtime = data['last_eruption_year'].max()
mintime = 1900
maxtime = 2030

app.layout =html.Div([    
                html.Div([
                     html.Div([
                         dcc.Graph(id='crash-map')
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
],style={'width':'100%'})    


@app.callback(
    Output(component_id='crash-map', component_property='figure'),
    [
        #Input(component_id='Organisation', component_property='value'),
        #Input(component_id='volcano_rocks', component_property='value'),
        Input(component_id='time-slider', component_property='value')
    ]
)
def update_output(time):
    mydata = data
    fig = px.scatter_mapbox(data_frame=mydata, 
                        lat=long,
                        lon=lat,
                        hover_data=["Organisation",
                                    "Crash_location_country",
                                    "Crash_location_city",
                                    "Date",
                                    "Year",
                                    "Ac_type"],
                        color='Total dead',
                        color_continuous_scale=px.colors.sequential.Bluered,
                        size='Total dead',
                        size_max=20,
                        zoom=1,
                        width = 1000,
                        height=800)
    print("plotly express hovertemplate:", fig.data[0].hovertemplate)
    fig.update_traces(hovertemplate = "<br>Organisation: %{customdata[0]}<br>Country: %{customdata[1]}<br>City: %{customdata[2]}<br>Date: %{customdata[3]} %{customdata[4]}<br>Aircraft type: %{customdata[5]}<extra></extra>")
    fig.update_layout(mapbox_style='carto-positron', autosize=False)
    fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    return fig
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)