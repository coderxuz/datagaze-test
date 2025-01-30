from pydantic import BaseModel, ConfigDict

class TokenRes(BaseModel):
    accessToken:str
    refreshToken:str

class UserSign(BaseModel):
    name: str
    surname: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class WeatherResponse(BaseModel):
    name: str
    country: str
    lat: float
    lon: float
    temp_c: float
    temp_color: str
    wind_kph: float
    wind_color: str
    cloud: int
    cloud_color: str
    
    
    model_config = ConfigDict(from_attributes=True)