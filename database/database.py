from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, WeatherData
from config.config import Config

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_weather_data(self, data):
        session = self.Session()
        try:
            weather_data = WeatherData(**data)
            session.add(weather_data)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error saving data: {e}")
            return False
        finally:
            session.close()
    
    def get_weather_data(self, city, limit=24):
        session = self.Session()
        try:
            return session.query(WeatherData)\
                         .filter(WeatherData.city == city)\
                         .order_by(WeatherData.timestamp.desc())\
                         .limit(limit)\
                         .all()
        finally:
            session.close()