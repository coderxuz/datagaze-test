import aiohttp
from dotenv import load_dotenv

import asyncio
from os import getenv
from pprint import pprint
from datetime import datetime
import asyncio

load_dotenv()

from app.models import WeatherData
from app.database import get_async_db

KEY = getenv("KEY")
if not KEY:
    raise ValueError("KEY didn't find")


country_list: list[str] = [
        "Afghanistan",
        "Albania",
        "Algeria",
        "Andorra",
        "Angola",
        "Antigua and Barbuda",
        "Argentina",
        "Armenia",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bhutan",
        "Bolivia",
        "Bosnia and Herzegovina",
        "Botswana",
        "Brazil",
        "Brunei",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Central African Republic",
        "Chad",
        "Chile",
        "China",
        "Colombia",
        "Comoros",
        "Congo",
        "Costa Rica",
        "Croatia",
        "Cuba",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Djibouti",
        "Dominica",
        "Dominican Republic",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Eritrea",
        "Estonia",
        "Eswatini",
        "Ethiopia",
        "Fiji",
        "Finland",
        "France",
        "Gabon",
        "Gambia",
        "Georgia",
        "Germany",
        "Ghana",
        "Greece",
        "Grenada",
        "Guatemala",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Honduras",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Ireland",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Kiribati",
        "Korea, North",
        "Korea, South",
        "Kuwait",
        "Kyrgyzstan",
        "Laos",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall Islands",
        "Mauritania",
        "Mauritius",
        "Mexico",
        "Micronesia",
        "Moldova",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Morocco",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nauru",
        "Nepal",
        "Netherlands",
        "New Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "North Macedonia",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines",
        "Poland",
        "Portugal",
        "Qatar",
        "Romania",
        "Russia",
        "Rwanda",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Samoa",
        "San Marino",
        "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "Somalia",
        "South Africa",
        "South Sudan",
        "Spain",
        "Sri Lanka",
        "Sudan",
        "Suriname",
        "Sweden",
        "Switzerland",
        "Syria",
        "Taiwan",
        "Tajikistan",
        "Tanzania",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tonga",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United Arab Emirates",
        "United Kingdom",
        "United States",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Vatican City",
        "Venezuela",
        "Vietnam",
        "Yemen",
        "Zambia",
        "Zimbabwe",
    ]

def get_temp_color(temp_c: int):
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


def get_wind_color(wind_kph: int):
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


def get_cloud_color(cloud_percentage: int):
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


async def search_weather(q: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://api.weatherapi.com/v1/current.json",
            params={"q": q},
            headers={"key": KEY},
        ) as response:
            if response.status == 200:
                data = await response.json()
                result = {
                    "name": data.get("location").get("name"),
                    "country": data.get("location").get("country"),
                    "lat": data.get("location").get("lat"),
                    "lon": data.get("location").get("lon"),
                    "temp_c": data.get("current").get("temp_c"),
                    "temp_color": get_temp_color(data.get("current").get("temp_c")),
                    "wind_kph": data.get("current").get("wind_kph"),
                    "wind_color": get_wind_color(data.get("current").get("wind_kph")),
                    "cloud": data.get("current").get("cloud"),
                    "cloud_color": get_cloud_color(data.get("current").get("cloud")),
                }
                pprint(result)
                return result
            else:
                pprint(response.status)
                pprint(await response.json())
                if response.status == 400:
                    return {"error": "bad request"}
                if response.status == 500:
                    return {"error": "error in weather server"}
                if response.status == 401:
                    return {"error": "token has expired"}
                return {"error": "error in server"}


async def save_weathers_to_db():
    current_time= datetime.now().date()
    print(current_time)
    async for session in get_async_db():
        for country in country_list:
            weather = await search_weather(q=country)
            if not weather.get("error"):
                new_weather = WeatherData(
                    name=weather.get("name"),
                    country=weather.get("country"),
                    lat=weather.get("lat"),
                    lon=weather.get("lon"),
                    temp_c=weather.get("temp_c"),
                    temp_color=weather.get("temp_color"),
                    wind_kph=weather.get("wind_kph"),
                    wind_color=weather.get("wind_color"),
                    cloud=weather.get("cloud"),
                    cloud_color=weather.get("cloud_color"),
                    created_at = current_time
                )
                session.add(new_weather)
                await session.commit()
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(save_weathers_to_db())
