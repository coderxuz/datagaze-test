from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
import pytest

client = TestClient(app)

@pytest.mark.asyncio
async def test_weather_get():
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MzgyNDMyMjB9.5F4P3STNyH0NNDhZEJim3mYh-e2dbYOWi1j0qCVjrWo"
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000") as client:
        response = await client.get('/weather', headers=headers, params={'country_name': "Afghanistan"})
    assert response.status_code == 200