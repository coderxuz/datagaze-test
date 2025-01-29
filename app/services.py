import aiohttp
from dotenv import load_dotenv

import asyncio
from os import getenv
from pprint import pprint
load_dotenv()

KEY = getenv('KEY')
if not KEY:
    raise ValueError("KEY didn't find")

def get_temp_color(temp_c):
    if temp_c <= -30:
        return "#003366"
    elif temp_c <= -20:
        return "#4A90E2"
    elif temp_c <= -10:
        return "#B3DFFD"
    elif temp_c < 0:
        return "#E6F7FF"
    elif temp_c < 10:
        return "#D1F2D3"
    elif temp_c < 20:
        return "#FFFACD"
    elif temp_c < 30:
        return "#FFCC80"
    elif temp_c < 40:
        return "#FF7043"
    else:
        return "#D32F2F"

def get_wind_color(wind_kph):
    if wind_kph <= 10:
        return "#E0F7FA"  # Light Cyan
    elif wind_kph <= 20:
        return "#B2EBF2"  # Pale Blue
    elif wind_kph <= 40:
        return "#4DD0E1"  # Soft Teal
    elif wind_kph <= 60:
        return "#0288D1"  # Bright Blue
    else:
        return "#01579B"  # Deep Navy Blue

def get_cloud_color(cloud_percentage):
    if cloud_percentage <= 10:
        return "#FFF9C4"  # Light Yellow
    elif cloud_percentage <= 30:
        return "#FFF176"  # Soft Yellow
    elif cloud_percentage <= 60:
        return "#E0E0E0"  # Light Gray
    elif cloud_percentage <= 90:
        return "#9E9E9E"  # Gray
    else:
        return "#616161"  # Dark Gray

async def search_weather(q:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://api.weatherapi.com/v1/forecast.json', params={"q":q, "days":1}, headers ={"key":KEY} ) as response:
            if response.status == 200:
                data:dict[str,str|dict|int,float] = await response.json()
                result = {
                    "name":data.get('location').get('name'),
                    "country":data.get('location').get('country'),
                    "lat":data.get('location').get('lat'),
                    "lon":data.get('location').get('lon'),
                    "temp_c":data.get('current').get('temp_c'),
                    "temp_color":get_temp_color(data.get('current').get('temp_c')),
                    "wind_kph":data.get('current').get('wind_kph'),
                    "wind_color":get_wind_color(data.get('current').get('wind_kph')),
                    "cloud":data.get('current').get('cloud'),
                    "cloud_color":get_cloud_color(data.get('current').get('cloud'))
                }
            else:
                if response.status == 400:
                    return {'error':"bad request"}
                if response.status == 500:
                    return {'error':"error in weather server"}
                if response.status == 401:
                    return {'error':"token has expired"}
                return {'error':"error in server"}


if __name__ == "__main__":
    asyncio.run(search_weather('Uzbekigfhstan'))

