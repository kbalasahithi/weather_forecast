import time
from config.config import Config
from database.database import DatabaseManager
from api.weather_api import WeatherAPI
from visualization.charts import WeatherDashboard
import threading

def update_weather_data(db_manager, weather_api):
    while True:
        for city in Config.CITIES:
            data = weather_api.get_weather_data(city)
            if data:
                db_manager.save_weather_data(data)
        time.sleep(Config.UPDATE_INTERVAL)

def main():
    # Initialize components
    db_manager = DatabaseManager()
    weather_api = WeatherAPI()
    dashboard = WeatherDashboard(db_manager)
    
    # Start weather data update thread
    update_thread = threading.Thread(
        target=update_weather_data,
        args=(db_manager, weather_api),
        daemon=True
    )
    update_thread.start()
    
    # Run the dashboard
    dashboard.run(debug=True)

if __name__ == "__main__":
    main()