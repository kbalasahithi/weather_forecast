import requests
from datetime import datetime
from config.config import Config

class WeatherAPI:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_API_URL
    
    def get_weather_data(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'city': city,
                'timestamp': datetime.now(),
                'temperature': data['list'][0]['main']['temp'],
                'humidity': data['list'][0]['main']['humidity'],
                'pressure': data['list'][0]['main']['pressure'],
                'description': data['list'][0]['weather'][0]['description']
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None