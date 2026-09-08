import secrets
import time
from email.message import EmailMessage
import smtplib
import ssl
import os
from Schemas.auth_email_schema import auth_email_schema
from dotenv import load_dotenv
from pathlib import Path
#--------------

#인증 번호 저장 변수 선언
contify_code = {}

# 프로젝트 최상위 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

#.env 파일 읽기
load_dotenv(BASE_DIR / ".env")

# .env에서 발송 메일 정보 가져오기
sender_email = os.getenv("GMAIL_ADDRESS")
password = os.getenv("GMAIL_APP_PASSWORD")

#인증 번호 만들고 발송해 주는 함수
def make_and_send_email_number(user_email:auth_email_schema) -> str:

    #인증 번호 생성
    email_number = f"{secrets.randbelow(1_000_000):06d}"

     #인증 번호 만료 시간 계산
    expires_at = time.monotonic() + 300
    
    #인증번호, 만료 시간 저장
    contify_code[user_email.email] = {
        "email_code":email_number,
        "expires_at":expires_at
    }

    #메세지 변수 선언
    message = EmailMessage()
    
    #이메일 메세지 작성
    message["From"] = sender_email
    message["To"] = user_email.email
    message["Subject"] = "J.H.Y-이메일 인증번호"
    message.set_content("인증 번호는 "+contify_code[user_email.email]["email_code"]+" 입니다.")

    #Gmail SMTP 연결 및 발송
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=context,
        timeout=10,
    ) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(message)
    
    return {
        "success":True
    }


#인증 번호 검증 함수
def check_email_number(user_code:str):

    #기존 email 인증 검증
    code = contify_code.get(user_code.email)
    
    #기존 인증 여부 검증
    if code is None:
        return {
            "success":False,
            "massage":"이메일이 옳지 않습니다."
        }

    #만료 시간 검증
    if time.monotonic() >= code["expires_at"]:
        contify_code.pop(user_code.email, None)
        return  {
        "success":False,
        "massage":"시간 초과"
    }

    #인증 번호 일치 여부 검증
    if code["email_code"] != user_code.code:
        return {
            "success":False,
            "massage":"인증 실패"
        }

    #인증 번호 삭제
    contify_code.pop(user_code.email, None)
    
    return {
        "success":True,
        "massage":"인증 성공"
    }
