import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from config.config import Config

class WeatherDashboard:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.app = Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Weather Forecast Dashboard"),
            
            # City management section
            html.Div([
                dcc.Input(
                    id='new-city-input',
                    type='text',
                    placeholder='Enter city name (e.g., Parker, CO)',
                    className='input-field'
                ),
                html.Button('Add City', id='add-city-button', n_clicks=0),
            ], className='city-management'),
            
            # City selection dropdown
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in Config.CITIES],
                value=Config.CITIES[0] if Config.CITIES else None,
                className='city-dropdown'
            ),
            
            # Weather graphs
            dcc.Graph(id='temperature-graph'),
            dcc.Graph(id='humidity-graph'),
            
            # Update interval
            dcc.Interval(
                id='interval-component',
                interval=Config.UPDATE_INTERVAL * 1000,
                n_intervals=0
            )
        ])
    
    def setup_callbacks(self):
        # Existing callback for graphs
        @self.app.callback(
            [Output('temperature-graph', 'figure'),
             Output('humidity-graph', 'figure')],
            [Input('city-dropdown', 'value'),
             Input('interval-component', 'n_intervals')]
        )
        def update_graphs(city, n):
            if not city:
                return {}, {}
                
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
        
        # New callback for adding cities
        @self.app.callback(
            [Output('city-dropdown', 'options'),
             Output('new-city-input', 'value')],
            [Input('add-city-button', 'n_clicks')],
            [State('new-city-input', 'value')]
        )
        def add_new_city(n_clicks, new_city):
            if n_clicks > 0 and new_city:
                Config.add_city(new_city)
                
            return [{'label': city, 'value': city} for city in Config.CITIES], ''
    
    def run(self, debug=False):
        self.app.run_server(debug=debug)

class CityManager:
    def __init__(self):
        self.cities = Config.CITIES
    
    def add_city(self, city_name):
        """Add a new city to track"""
        Config.add_city(city_name)
        
    def remove_city(self, city_name):
        """Remove a city from tracking"""
        Config.remove_city(city_name)
        
    def get_cities(self):
        """Get list of all tracked cities"""
        return Config.CITIES

# Add some CSS styles
CUSTOM_STYLES = """
.city-management {
    margin: 20px 0;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.input-field {
    margin-right: 10px;
    padding: 5px;
}

.city-dropdown {
    margin: 20px 0;
}
"""