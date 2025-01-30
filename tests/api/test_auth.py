from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# def test_sign():
#     response = client.post(
#         "/auth/sign",
#         json={
#             "name": "string1",
#             "surname": "string1",
#             "username": "string1",
#             "password": "string1",
#         },
#     )
#     assert response.status_code == 200
#     assert "accessToken" in response.json()
#     assert "refreshToken" in response.json()

def test_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "string1",
            "password": "string1",
        },
    )
    assert response.status_code == 200
    assert "accessToken" in response.json()
    assert "refreshToken" in response.json()

