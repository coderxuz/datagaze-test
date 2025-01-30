Datagaze task for backend


1️⃣ Endpoint /auth/sign
    - Method:POST
    - Description: Endpoint for registering
    - Request Body: JSON
    
    ✅ Example Request:
    POST /auth/sign
    Content-Type: application/json

    {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe123",
        "password": "SecurePass123!"
    }   

    ✅ Example Response:

    {
        "accessToken": "your_access_token_here",
        "refreshToken": "your_refresh_token_here"
    }

---

2️⃣ Endpoint: /auth/login

    - Method:POST
    - Description: Endpoint for login
    - Request Body: JSON3️
    
    ✅ Example Request:
    POST /auth/sign
    Content-Type: application/json

    {
        "username": "johndoe123",
        "password": "SecurePass123!"
    }   

    ✅ Example Response:
    
    {
        "accessToken": "your_access_token_here",
        "refreshToken": "your_refresh_token_here"
    }

3️⃣ Endpoint: /weather

    - Method:GET
    - Description: Endpoint for getting today's weather with search 
    - Request Body: JSON3️
    - Query Parametr:
        country_name:string (required)
    
    ✅ Example Request:
    GET /weather?country_name=New%20York
    Content-Type: application/json
    Authorization:Bearer accessToken

    ✅ Example Response:
    
    {
        "name": "New York",
        "country": "United States of America",
        "lat": 40.7142,
        "lon": -74.0064,
        "temp_c": -3.3,
        "temp_color": "#E6F7FF",
        "wind_kph": 19.4,
        "wind_color": "#B2EBF2",
        "cloud": 0,
        "cloud_color": "#FFF9C4"
    }
