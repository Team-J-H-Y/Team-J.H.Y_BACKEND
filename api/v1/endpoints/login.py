from fastapi import HTTPException, Depends, APIRouter, Response
from models.users import Users
from sqlalchemy.orm import Session
from models.session_model import Session_Model
from Schemas.login_schema import loginData
from database.connection import Create_db
from sqlalchemy import select
from pwdlib import PasswordHash
import secrets
from datetime import datetime, timedelta, timezone
#--------------------------------

#라우터 연결
router_login = APIRouter()

#혜시 객체 생성
password_hashing = PasswordHash.recommended()

@router_login.post("/api/v1/users/login")
def login(login_data: loginData,response : Response, db: Session = Depends(Create_db)):

    #사용자 조회
    user = db.scalar(
        select(Users).where(Users.email == login_data.email)
    )

    if user is None:
        return HTTPException(
            status_code = 401,
            detail = "아이디 또는 비밀번호가 올바르지 않습니다. 입력한 정보를 다시 확인해 주세요."
        )

    #비밀번호 검증
    is_correct = password_hashing.verify(
        login_data.password,
        user.password_hash
    )

    if is_correct is False:
        return HTTPException(
            status_code = 401,
            detail = "아이디 또는 비밀번호가 올바르지 않습니다. 입력한 정보를 다시 확인해 주세요."
        )

    #세션 존재 여부 검증
    #세션 객체 조회
    user_session = db.get(
        Session_Model,
        login
    )
    
    
    #만료 여부 검사
    if user_session.expired_at <= datetime.now(timezone.utc) | user_session is None:
        db.delete(user_session)
        db.commit()
        create_session(user,response, db)

    #기존 세션 쿠키 지정
    else:
        response.set_cookie(
            key="Session_id",
            value=user_session.session_id, #실제 세션 값
            max_age=user_session.expired_at, #세션 만료기간, 자동 로그인 유지 기간
            httponly=True, #js에서 쿠키 접근 제한
            secure=False, #HTTPS에서만 Cookie 전송 제한
            samesite="lax", #교차 사이트 Cookie 전송 일부 제한
            path="/" #모든 API경로에서 Cookie 사용
        )

    return {
        "message": "로그인 성공"
    }


#세션 생성 함수
def create_session(user,response : Response,db: Session):
    #세션 생성
    Session_data = secrets.token_urlsafe(32)
    
    #만료기한 계산
    time_now = datetime.now(timezone.utc) #현재 시간 계산
    lifetime = timedelta(days=1) #만료 기한 설정
    expire = time_now + lifetime #만료 기한 계산
    
    #세션 객체 생성
    new_Session = Session_Model(
        Session_id = Session_data,
        user_id = user.user_id,
        created_at = time_now,
        expired_at = expire
    )
    
    #세션 객체 저장
    db.add(new_Session)
    db.commit()
    
    #쿠키 지정
    response.set_cookie(
        key="Session_id",
        value=Session_data, #실제 세션 값
        max_age=expire, #세션 만료기간, 자동 로그인 유지 기간
        httponly=True, #js에서 쿠키 접근 제한
        secure=False, #HTTPS에서만 Cookie 전송 제한
        samesite="lax", #교차 사이트 Cookie 전송 일부 제한
        path="/" #모든 API경로에서 Cookie 사용
    )
    
    pass
    