import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_confirmed = 'time_series_covid19_confirmed_SD.csv'
url_deaths = 'time_series_covid19_deaths_SD.csv'
url_recovered = 'time_series_covid19_recovered_SD.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# Unpivot data frames
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province_State', 'Admin2', 'Lat', 'Long_'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province_State', 'Admin2', 'Lat', 'Long_'], value_vars=date2, var_name='date', value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province_State', 'Admin2', 'Lat', 'Long_'], value_vars=date3, var_name='date', value_name='recovered')

# Merging data frames
covid_data = total_confirmed.merge(right=total_deaths, how='left', on=['Province_State', 'Admin2', 'date', 'Lat', 'Long_'])
covid_data = covid_data.merge(right=total_recovered, how='left', on=['Province_State', 'Admin2', 'date', 'Lat', 'Long_'])

# Converting date column from string to proper date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

# Check how many missing value naN
covid_data.isna().sum()

# Replace naN with 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# Calculate new column
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

# create dictionary of list
covid_data_dict = covid_data[['Admin2', 'Lat', 'Long_']]
list_locations = covid_data_dict.set_index('Admin2')[['Lat', 'Long_']].T.to_dict('dict')


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),
                     id='corona-image',
                     style={
                         "height": "150px",
                         "width": "auto",
                         "margin-bottom": "150px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("Covid - 19", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Track Covid - 19 Cases", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6('Last Updated: ' + str(covid_data_1['date'].iloc[-1].strftime("%B %d, %Y")) + '  00:01 (UTC)',
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='SD Cases',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{covid_data_1['confirmed'].iloc[-1]:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) /
                                       covid_data_1['confirmed'].iloc[-1]) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='SD Deaths',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{covid_data_1['death'].iloc[-1]:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]) /
                                       covid_data_1['death'].iloc[-1]) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='SD Recovered',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{covid_data_1['recovered'].iloc[-1]:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]) /
                                       covid_data_1['recovered'].iloc[-1]) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='SD Active',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{covid_data_1['active'].iloc[-1]:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) /
                                       covid_data_1['active'].iloc[-1]) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns")

    ], className="row flex-display"),

    html.Div([
        html.Div([

                    html.P('Select County:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='w_counties',
                                  multi=False,
                                  clearable=True,
                                  value='Aurora',
                                  placeholder='Select Counties',
                                  options=[{'label': c, 'value': c}
                                           for c in (covid_data['Admin2'].unique())], className='dcc_compon'),

                     html.P('New Cases : ' + '  ' + ' ' + str(covid_data_2['date'].iloc[-1].strftime("%B %d, %Y")) + '  ', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
                     dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'},
                     ),

                      dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

        ], className="create_container three columns", id="cross-filter-options"),
            html.Div([
                      dcc.Graph(id='pie_chart',
                              config={'displayModeBar': 'hover'}),
                              ], className="create_container four columns"),

                    html.Div([
                        dcc.Graph(id="line_chart")

                    ], className="create_container five columns"),

        ], className="row flex-display"),

html.Div([
        html.Div([
            dcc.Graph(id="map")], className="create_container1 twelve columns"),

            ], className="row flex-display"),

    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('confirmed', 'figure'),
    [Input('w_counties', 'value')])
def update_confirmed(w_counties):
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_confirmed = covid_data_2[covid_data_2['Admin2'] == w_counties]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Admin2'] == w_counties]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Admin2'] == w_counties]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Admin2'] == w_counties]['confirmed'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_confirmed,
                    delta={'reference': delta_confirmed,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Confirmed',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='orange'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('death', 'figure'),
    [Input('w_counties', 'value')])
def update_confirmed(w_counties):
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_death = covid_data_2[covid_data_2['Admin2'] == w_counties]['death'].iloc[-1] - covid_data_2[covid_data_2['Admin2'] == w_counties]['death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Admin2'] == w_counties]['death'].iloc[-2] - covid_data_2[covid_data_2['Admin2'] == w_counties]['death'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_death,
                    delta={'reference': delta_death,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Death',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#dd1e35'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('recovered', 'figure'),
    [Input('w_counties', 'value')])
def update_confirmed(w_counties):
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_recovered = covid_data_2[covid_data_2['Admin2'] == w_counties]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Admin2'] == w_counties]['recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Admin2'] == w_counties]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Admin2'] == w_counties]['recovered'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_recovered,
                    delta={'reference': delta_recovered,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Recovered',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='green'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('active', 'figure'),
    [Input('w_counties', 'value')])
def update_confirmed(w_counties):
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_active = covid_data_2[covid_data_2['Admin2'] == w_counties]['active'].iloc[-1] - covid_data_2[covid_data_2['Admin2'] == w_counties]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Admin2'] == w_counties]['active'].iloc[-2] - covid_data_2[covid_data_2['Admin2'] == w_counties]['active'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_active,
                    delta={'reference': delta_active,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Active',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#e55467'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

# Create pie chart (total casualties)
@app.callback(Output('pie_chart', 'figure'),
              [Input('w_counties', 'value')])

def update_graph(w_counties):
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    new_confirmed = covid_data_2[covid_data_2['Admin2'] == w_counties]['confirmed'].iloc[-1]
    new_death = covid_data_2[covid_data_2['Admin2'] == w_counties]['death'].iloc[-1]
    new_recovered = covid_data_2[covid_data_2['Admin2'] == w_counties]['recovered'].iloc[-1]
    new_active = covid_data_2[covid_data_2['Admin2'] == w_counties]['active'].iloc[-1]
    colors = ['orange', '#dd1e35', 'green', '#e55467']

    return {
        'data': [go.Pie(labels=['Confirmed', 'Death', 'Recovered', 'Active'],
                        values=[new_confirmed, new_death, new_recovered, new_active],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                        # insidetextorientation='radial',


                        )],

        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'Total Cases : ' + (w_counties),


                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
            ),


        }

# Create bar chart (show new cases)
@app.callback(Output('line_chart', 'figure'),
              [Input('w_counties', 'value')])
def update_graph(w_counties):
# main data frame
    covid_data_2 = covid_data.groupby(['date', 'Admin2'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
# daily confirmed
    covid_data_3 = covid_data_2[covid_data_2['Admin2'] == w_counties][['Admin2', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()

    return {
        'data': [go.Bar(x=covid_data_3[covid_data_3['Admin2'] == w_counties]['date'].tail(30),
                        y=covid_data_3[covid_data_3['Admin2'] == w_counties]['daily confirmed'].tail(30),

                        name='Daily confirmed',
                        marker=dict(
                            color='orange'),
                        hoverinfo='text',
                        hovertext=
                        '<b>Date</b>: ' + covid_data_3[covid_data_3['Admin2'] == w_counties]['date'].tail(30).astype(str) + '<br>' +
                        '<b>Daily confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Admin2'] == w_counties]['daily confirmed'].tail(30)] + '<br>' +
                        '<b>County</b>: ' + covid_data_3[covid_data_3['Admin2'] == w_counties]['Admin2'].tail(30).astype(str) + '<br>'


                        ),
                 go.Scatter(x=covid_data_3[covid_data_3['Admin2'] == w_counties]['date'].tail(30),
                            y=covid_data_3[covid_data_3['Admin2'] == w_counties]['Rolling Ave.'].tail(30),
                            mode='lines',
                            name='Rolling average of the last seven days - daily confirmed cases',
                            line=dict(width=3, color='#FF00FF'),
                            # marker=dict(
                            #     color='green'),
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Admin2'] == w_counties]['date'].tail(30).astype(str) + '<br>' +
                            '<b>Rolling Ave.(last 7 days)</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Admin2'] == w_counties]['Rolling Ave.'].tail(30)] + '<br>'
                            )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Last 30 Days Confirmed Cases : ' + (w_counties),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 20},

             hovermode='x',
             margin = dict(r = 0),
             xaxis=dict(title='<b>Date</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b>Daily confirmed Cases</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                ),

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),

                 )

    }

# Create scattermapbox chart
@app.callback(Output('map', 'figure'),
              [Input('w_counties', 'value')])
def update_graph(w_counties):
    covid_data_3 = covid_data.groupby(['Lat', 'Long_', 'Admin2'])[['recovered', 'death', 'confirmed', 'active']].max().reset_index()
    covid_data_4 = covid_data_3[covid_data_3['Admin2'] == w_counties]

    if w_counties:
        zoom = 2
        zoom_lat = list_locations[w_counties]['Lat']
        zoom_lon = list_locations[w_counties]['Long_']

    return {
        'data': [go.Scattermapbox(
                         lon=covid_data_4['Long_'],
                         lat=covid_data_4['Lat'],
                         mode='markers',
                         marker=go.scattermapbox.Marker(
                                  size=covid_data_4['confirmed'] / 1500,
                                  color=covid_data_4['confirmed'],
                                  colorscale='hsv',
                                  showscale=False,
                                  sizemode='area',
                                  opacity=0.3),

                         hoverinfo='text',
                         hovertext=
                         '<b>County</b>: ' + covid_data_4['Admin2'].astype(str) + '<br>' +
                         '<b>Longitude</b>: ' + covid_data_4['Long_'].astype(str) + '<br>' +
                         '<b>Latitude</b>: ' + covid_data_4['Lat'].astype(str) + '<br>' +
                         '<b>Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_4['confirmed']] + '<br>' +
                         '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_4['death']] + '<br>' +
                         '<b>Recovered</b>: ' + [f'{x:,.0f}' for x in covid_data_4['recovered']] + '<br>' +
                         '<b>Active</b>: ' + [f'{x:,.0f}' for x in covid_data_4['active']] + '<br>'

                        )],


        'layout': go.Layout(
             margin={"r": 0, "t": 0, "l": 0, "b": 0},
             # width=1820,
             # height=650,
             hovermode='closest',
             mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_lon),
                # style='open-street-map',
                style='dark',
                zoom=zoom
             ),
             autosize=True,

        )

    }

if __name__ == '__main__':
    app.run_server(debug=True)
