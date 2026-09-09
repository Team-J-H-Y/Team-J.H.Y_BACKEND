from pydantic import BaseModel

#비밀번호 잋음
class password_forget(BaseModel):
    email: str
    name: str
    number: str