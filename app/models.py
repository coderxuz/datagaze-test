from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    name: Mapped[str]
    surname: Mapped[str] 
    username: Mapped[str] =mapped_column(unique=True) 
    password: Mapped[str]

    
class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    name: Mapped[str]
    country: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
    temp_c: Mapped[float]
    temp_color: Mapped[str]
    wind_kph: Mapped[float]
    wind_color: Mapped[str]
    cloud: Mapped[int]
    cloud_color: Mapped[str]
    created_at:Mapped[datetime]

if __name__ == '__main__':
    Base.metadata.create_all(engine)