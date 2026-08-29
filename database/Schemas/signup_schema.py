from pydantic import BaseModel

#센서값 스키마
class SignupData(BaseModel):
    user_id: str
    password_hash: str
    name: str
    number: str
    email: str