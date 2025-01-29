from pydantic import BaseModel

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