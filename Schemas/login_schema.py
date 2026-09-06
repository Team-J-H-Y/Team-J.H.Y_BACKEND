from pydantic import BaseModel

#로그인 스키마
class loginData(BaseModel):
    password: str
    email: str