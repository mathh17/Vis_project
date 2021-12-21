#%%
#from numpy import absolute
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import sys
#%%
path = sys.path
data = pd.read_csv(path[0]+'\\crashes_to_visualize.csv') #Dash
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

countries = data['Crash_location_country'].unique()

countries_options = [{'label': i, 'value': i} for i in countries]
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
months_options = [{'label': i, 'value': i} for i in months]

app.layout =html.Div([
                html.H1(children="The World's Plane Crashes",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),    
                html.Div([
                        html.Div([
                            dcc.Graph(id='crash-map',style={"width":"40%","display":"block"}),
                            html.P(["Filter by organisations, countries, months and years"],style={'margin-left':'20px'}),
                            dcc.Dropdown(
                            id='organisation',
                            options=type_options,
                            value=[],
                            placeholder = "Organisations",
                            multi = True,
                            style={'width':'900px','margin-left':'10px',"margin-top":"10px","display":"block"}),
                            dcc.Dropdown(
                            id='country_options',
                            options=countries_options,
                            value=[],
                            placeholder = "Countries",
                            multi = True,
                            style={'width':'900px','margin-left':'10px',"margin-top":"10px","display":"block"}),
                            dcc.Dropdown(
                            id='month',
                            options=months_options,
                            value=[],
                            placeholder = "Months",
                            multi = True,
                            style={'width':'900px','margin-left':'10px',"margin-top":"10px","display":"block"}),
                        html.Div([
                            dcc.RangeSlider(
                            id='time-slider',
                            min=mintime,
                            max=maxtime,
                            step=1,
                            value=[mintime,maxtime],
                            tooltip={"placement": "bottom", "always_visible": True})],style={"width":"950px","display":"block","margin-top": "5px"})],style={"display":"inline"}),
                        html.Div([
                            dcc.Graph(id='org_chart',style={'width':'40%','margin-left':'1100px',"border":"2px solid","display":"inline-block"}),
                            dcc.Graph(id='death_chart',style={'width':'40%','margin-left':'1100px',"border":"2px solid","display":"inline-block"}),
                            html.Div([
                            dcc.Graph(id='pie_chart',style={}),
                            html.Div([
                            html.P(id='org_info'),
                            html.P(id='route'),
                            html.P(id='country_info'),
                            html.P(id='date_info'),
                            html.P(id='death_text'),
                            "Summary about the crash:",
                            html.P(id='Summary_area')],style={'margin-left':'20px'})],style={'width':'40%','margin-left':'1100px',"border":"2px solid","display":"inline-block"})]
                            ,style={'width':'400',"margin-top":"-950px","display":"block",'float':'right'}),
                ])
])
    
@app.callback(
    Output('pie_chart','figure'),
    Output('Summary_area', 'children'),
    Output('org_info', 'children'),
    Output('country_info', 'children'),
    Output('date_info', 'children'),
    Output('death_text', 'children'),
    Output('route', 'children'),
    [
        Input('crash-map','clickData'),
    ])
def click_updater(click_data): 
    if click_data != None:
        custom_data = click_data['points'][0]['customdata']
        org_text = "Organisation: " + custom_data[0] + " Aircraft type: " +custom_data[5] #+ " Crash_location_city: " + custom_data[2] + " Date: " + custom_data[3] +" Year:"+custom_data[4]+" Total deaths: "+ custom_data[7]
        country_text = "Country/Stage: "+custom_data[1]+" City: " + custom_data[2]
        date_text = "Date: " + str(custom_data[3])+" "+custom_data[12] +" "+str(custom_data[4])
        death_text = "Total deaths: "+ str(custom_data[14])
        route = "Route: "+custom_data[15]
        summary_text = custom_data[11]
        fig_2 = px.pie(data_frame=click_data, 
                values=[custom_data[6],
                custom_data[7],
                custom_data[8],
                custom_data[9],
                custom_data[10]],
                names= ['Dead passengers','Dead crew','Surviving passengers','Surviving crew','People killed on ground'],
                color=['Dead passengers','Dead crew','Surviving passengers','Surviving crew','People killed on ground'],
                title='Crash information',
                color_discrete_map={'Dead passengers':'#e74127',
                'Dead crew':'#e77a27',
                'Surviving passengers':'#91e842',
                'Surviving crew':'#14a338',
                'People killed on ground':'#a51f12'})
    return fig_2, summary_text, org_text, country_text, date_text,death_text, route


@app.callback(
    Output(component_id='crash-map', component_property='figure'),
    Output(component_id='death_chart', component_property='figure'),
    Output(component_id='org_chart', component_property='figure'),
    [
        Input(component_id='time-slider', component_property='value'),
        Input(component_id='organisation', component_property='value'),
        Input(component_id='month',component_property='value'),
        Input(component_id='country_options',component_property='value'),        
    ]
)

def update_output(time, organisation, month, countries):
    mydata = data
    mydata['crash_count'] = 1
    print(len(month))
    if len(month) >= 1:
        mydata = mydata[mydata['Month'].isin(month)]
    if len(countries) >= 1:
        mydata = mydata[mydata['Crash_location_country'].isin(countries)]
    if len(organisation) >= 1:
        mydata = mydata[mydata['Organisation'].isin(organisation)]
    if len(organisation) == 0 and len(month) == 0 and len(countries) == 0:
        mydata = data
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
                                    'Ground_fatalities_num',
                                    'Summary',
                                    "Month",
                                    "Onboard deaths",
                                    "all deaths",
                                    "Route"],
                        color='Onboard deaths',
                        color_continuous_scale='plasma_r',
                        size=[max(10, i) for i in mydata['Onboard deaths']],
                        size_max=30,
                        zoom=1,
                        width = 1000,
                        height=750)
    #print("plotly express hovertemplate:", fig_1.data[0].hovertemplate)
    fig_1.update_traces(hovertemplate = "<br>Organisation: %{customdata[0]}<br>Country/State: %{customdata[1]}<br>City: %{customdata[2]}<br>Date: %{customdata[3]} %{customdata[12]} %{customdata[4]}<br>Aircraft type: %{customdata[5]}<extra></extra>")
    fig_1.update_layout(mapbox_style='carto-positron', autosize=False)
    fig_1.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    fig_2 = px.histogram(mydata,
                        x="Year",
                        nbins=time[1]-time[0],
                        y=['Passengers dead',
                            'Crew dead',
                            'Passengers survivors',
                            'Crew survivors',
                            'Ground_fatalities_num'], 
                        title='Distribution of fatalities',
                        height=400,
                        width=700)
    
    fig_3 = px.histogram(mydata,
                        x="Year",
                        nbins=time[1]-time[0],
                        y=['crash_count'],
                        color='Organisation',
                        labels="Flight_num", 
                        title='Number of crashes per organisation',
                        height=400,
                        width=750)
    fig_3.update_layout(showlegend=False)
    return fig_1, fig_2, fig_3

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)