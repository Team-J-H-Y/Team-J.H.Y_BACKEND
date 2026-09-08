from fastapi import APIRouter,Depends,HTTPException
from auth.auth_email_number import make_email_number
from Schemas.auth_email_schema import auth_email_schema
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.connection import Create_db
from models.users import Users
from Schemas.email_code_schema import email_code_schema
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import time
import os
import smtplib
import ssl
#-----------------------------

# 프로젝트 최상위 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

#.env 파일 읽기
load_dotenv(BASE_DIR / ".env")

# .env에서 발송 메일 정보 가져오기
sender_email = os.getenv("GMAIL_ADDRESS")
password = os.getenv("GMAIL_APP_PASSWORD")

#라우터 연결
router_email = APIRouter()

#인증 번호 저장 변수 선언
contify_code = {}

#이메일 인증 함수
@router_email.post("/api/v1/email")
def email_contify(user_email:auth_email_schema, db:Session = Depends(Create_db)):

    #이메일 중복 검사
    exist_user = db.scalar(
        select(Users).where(Users.email == user_email.email)
    )
    
    if exist_user is not None:
        return HTTPException(
            status_code = 409,
            detail = "이미 사용중인 이메일입니다."
        )

    #인증 번호 저장
    contify_code[user_email.email] = make_email_number(user_email.email)

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



#이메일 인증 번호 검증 함수
@router_email.post("/api/v1/email_code")
def email_code_check(user_code:email_code_schema,db:Session = Depends(Create_db)):

    #기존 email 인증 검증
    code = contify_code.get(user_code.email)

    #기존 인증 여부 검증
    if code is None:
        return {
        "success":False,
        "massage":"이미 존재하는 이메일"
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

    contify_code.pop(user_code.email, None)

    return {
        "success":True,
        "massage":"인증 성공"
    }