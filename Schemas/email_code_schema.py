from pydantic import BaseModel

#이메일 인증 번호 스키마
class email_code_schema(BaseModel):
    email: str
    code: str