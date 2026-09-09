from fastapi import Cookie, Depends, HTTPException, Response
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.users import Users
from models.session_model import Session_Model
from database.connection import Create_db
import secrets
from datetime import datetime, timedelta, timezone
#---------------------------------------------------

#세션 검증 및 사용자 객체 반환 함수
def check_session(session_id: str, db:Session)-> Users | None:

    #세션 객체 조회
    user_session = db.get(
        Session_Model,
        session_id
    )

    if user_session is None:
        return None

    #만료 여부 검사
    if user_session.expired_at <= datetime.now(timezone.utc):
        db.delete(user_session)
        db.commit()
        return None

    #일치하는 사용자 검증
    user = db.get(
        Users,
        user_session.user_id
    )

    if user is None:
        return None

    #사용자 반환
    return user

#세션 검증 함수 호출 함수
def get_current_user(session_id: str | None = Cookie(default=None),db: Session = Depends(Create_db)) -> Users:

    #세션 존재 여부 검사
    if session_id is None:
        raise HTTPException(                                                     
            status_code=401,
            detail="로그인이 필요합니다."
        )

    #세션 검증 함수 호출
    user = check_session(session_id, db)

    #검증 결과 반환
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않거나 만료된 세션입니다."
        )

    #사용자 반환
    return user

#세션 삭제 함수
def delete_session(session_id:str, db:Session) -> None:

    #세션 존재 여부 검증
    user_session = db.get(
        Session_Model,
        session_id
    )

    if user_session is None:
        return None

    #해당 세션 삭제
    db.delete(user_session)
    db.commit()



#세션 생성 함수
def create_session(user:str,response : Response,db: Session):
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
    

