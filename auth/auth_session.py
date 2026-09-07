from fastapi import Cookie, Depends, HTTPException
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.users import Users
from models.session_model import Session_Model
from database.connection import Create_db
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