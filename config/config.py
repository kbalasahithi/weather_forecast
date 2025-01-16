import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///weather_data.db')
    
    # Application Settings
    UPDATE_INTERVAL = 3600  # Update weather data every hour
    CITIES = ['London', 'New York', 'Tokyo', 'Paris', 'Sydney']