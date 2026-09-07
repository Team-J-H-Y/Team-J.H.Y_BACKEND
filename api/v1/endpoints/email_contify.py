from fastapi import APIRouter,Depends,HTTPException
from auth.auth_email_number import make_email_number
from Schemas.auth_email_schema import auth_email_schema
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.connection import Create_db
from models.users import Users
from Schemas.email_code_schema import email_code_schema

import time
#-----------------------------

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
    contify_code[user_email] = make_email_number(user_email)

#이메일 인증 번호 검증 함수
@router_email.post("/api/v1/email_code")
def email_code_check(user_code:email_code_schema,db:Session = Depends(Create_db)):

    #기존 email 인증 검증
    code = contify_code.get(user_code.email)

    #기존 인증 여부 검증
    if code is None:
        return None

    #만료 시간 검증
    if time.monotonic() >= code["expires_at"]:
        contify_code.pop(user_code.email, None)
        return None

    #인증 번호 일치 여부 검증
    if code["email_code"] != user_code.code:
        return None

    contify_code.pop(user_code.email, None)

    return {
        "massage":"인증 성공"
    }