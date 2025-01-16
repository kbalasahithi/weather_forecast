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
    
    # Default cities list with US state codes
    CITIES = [
        'Parker, CO',
        'Denver, CO',
        'Castle Rock, CO',
        'Aurora, CO',
        'Centennial, CO',
        'Boulder, CO',
        'Fort Collins, CO'
    ]
    
    @classmethod
    def add_city(cls, city):
        """Add a new city to the tracking list"""
        if city not in cls.CITIES:
            cls.CITIES.append(city)
    
    @classmethod
    def remove_city(cls, city):
        """Remove a city from the tracking list"""
        if city in cls.CITIES:
            cls.CITIES.remove(city)