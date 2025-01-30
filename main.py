from fastapi import FastAPI

from app.api import auth, weather

app = FastAPI()

@app.get('/')
async def root_endpoint():
    return {'message':"hello world"}

app.include_router(auth.router)
app.include_router(weather.router)