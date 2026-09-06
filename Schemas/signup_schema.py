from pydantic import BaseModel

#회원가입 스키마
class SignupData(BaseModel):
    password_hash: str
    name: str
    number: str
    email: str