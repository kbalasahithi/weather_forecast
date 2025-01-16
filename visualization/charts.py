import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

class WeatherDashboard:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.app = Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Weather Forecast Dashboard"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in Config.CITIES],
                value=Config.CITIES[0]
            ),
            dcc.Graph(id='temperature-graph'),
            dcc.Graph(id='humidity-graph'),
            dcc.Interval(
                id='interval-component',
                interval=Config.UPDATE_INTERVAL * 1000,
                n_intervals=0
            )
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
            [Output('temperature-graph', 'figure'),
             Output('humidity-graph', 'figure')],
            [Input('city-dropdown', 'value'),
             Input('interval-component', 'n_intervals')]
        )
        def update_graphs(city, n):
            data = self.db_manager.get_weather_data(city)
            df = pd.DataFrame([{
                'timestamp': d.timestamp,
                'temperature': d.temperature,
                'humidity': d.humidity
            } for d in data])
            
            temp_fig = px.line(df, x='timestamp', y='temperature',
                             title=f'Temperature in {city}')
            humid_fig = px.line(df, x='timestamp', y='humidity',
                              title=f'Humidity in {city}')
            
            return temp_fig, humid_fig
    
    def run(self, debug=False):
        self.app.run_server(debug=debug)