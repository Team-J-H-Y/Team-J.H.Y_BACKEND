from pydantic import BaseModel

#이메일 스키마
class auth_email_schema(BaseModel):
    email: str

