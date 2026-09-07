from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session as DBSession

from auth.auth_session import delete_session
from database.connection import Create_db
#--------------------------------------------------

#라우터 선언
router_logout = APIRouter()

#로그아웃 함수
@router_logout.post("/logout")
def logout(response: Response, session_id: str | None = Cookie(default=None), db: DBSession = Depends(Create_db)):
    if session_id is not None:
        delete_session(
            session_id=session_id,
            db=db
        )

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return {
        "message": "로그아웃되었습니다."
    }