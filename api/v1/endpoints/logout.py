from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session
from auth.auth_session import get_current_user
from auth.auth_session import delete_session
from database.connection import Create_db
from models.users import Users
#--------------------------------------------------

#라우터 선언
router_logout = APIRouter()

#로그아웃 함수
@router_logout.post("/api/v1/logout")
def logout(response: Response, session_id: Users  = Depends(get_current_user), db: Session = Depends(Create_db)):
    if session_id is not None:
        delete_session(
            session_id.user_id,
            db
        )

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return {
        "message": "로그아웃되었습니다."
    }