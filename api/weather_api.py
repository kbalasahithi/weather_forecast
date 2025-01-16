import requests
from datetime import datetime
from config.config import Config

class WeatherAPI:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_API_URL

    def format_city_name(self, city):
        """Format city name for API request"""
        # Remove state code for US cities
        if ', ' in city:
            city_name, state = city.split(', ')
            if state == 'CO':  # for Colorado cities
                return f"{city_name},US"  # OpenWeatherMap format for US cities
        return city

    def get_weather_data(self, city):
        formatted_city = self.format_city_name(city)
        params = {
            'q': formatted_city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            print(f"Requesting weather data for: {formatted_city}")  # Debug line
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Convert temperature from Celsius to Fahrenheit
            temp_celsius = data['list'][0]['main']['temp']
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            
            return {
                'city': city,  # Keep original city name for display
                'timestamp': datetime.now(),
                'temperature': temp_fahrenheit,  # Store in Fahrenheit
                'humidity': data['list'][0]['main']['humidity'],
                'pressure': data['list'][0]['main']['pressure'],
                'description': data['list'][0]['weather'][0]['description']
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None