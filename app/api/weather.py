from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import oauth2_scheme, auth
from app.database import get_async_db
from app.models import User, WeatherData
from app.schemas import WeatherResponse
from app.services import search_weather

from datetime import datetime

router = APIRouter(prefix="/weather", tags=["WEATHER"])


@router.get("", response_model=WeatherResponse)
async def get_weather(
    country_name: str,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db),
):
    subject = auth.get_subject(token=token)
    db_user = (
        (await db.execute(select(User).where(User.username == subject)))
        .scalars()
        .first()
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    current_time = datetime.now().date()
    exist_weather = (
        (
            await db.execute(
                select(WeatherData).where(
                    WeatherData.country.ilike(f"%{country_name}%"),
                    WeatherData.created_at == current_time,
                )
            )
        )
        .scalars()
        .first()
    )
    if exist_weather:
        print("weather found")
        return exist_weather
    weather_response = None
    if not exist_weather:
        weather_response = await search_weather(q=country_name)  # type:ignore
    if weather_response.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=weather_response.get("error"),
        )
    print("weather not exist in db")
    new_weather = WeatherData(
        name=weather_response.get("name"),
        country=weather_response.get("country"),
        lat=weather_response.get("lat"),
        lon=weather_response.get("lon"),
        temp_c=weather_response.get("temp_c"),
        temp_color=weather_response.get("temp_color"),
        wind_kph=weather_response.get("wind_kph"),
        wind_color=weather_response.get("wind_color"),
        cloud=weather_response.get("cloud"),
        cloud_color=weather_response.get("cloud_color"),
        created_at=current_time,
    )
    db.add(new_weather)
    await db.commit()
    return weather_response
