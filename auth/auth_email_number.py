import secrets
import time

from Schemas.auth_email_schema import auth_email_schema
#--------------

#인증 번호 만들어주는 함수
def make_email_number(email:auth_email_schema) -> str:

    #인증 번호 생성
    email_number = f"{secrets.randbelow(1_000_000):06d}"

     #인증 번호 만료 시간 계산
    expires_at = time.monotonic() + 300
    
    #인증번호, 만료 시간 저장
    contify_code = {
        "email_code":email_number,
        "expires_at":expires_at
    }

    return contify_code

