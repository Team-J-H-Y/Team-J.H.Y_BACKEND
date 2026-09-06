from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from pwdlib import PasswordHash
from database.connection import Create_db
from Schemas.signup_schema import SignupData
from models.users import Users

#--------------------------------

#라우터 연결
router_signup = APIRouter()

#혜시 객체 생성
password_hashing = PasswordHash.recommended()

#회원가입 API
@router_signup.post("/api/v1/users/signup")
def signup(User_data: SignupData, db: Session = Depends(Create_db)):

    #이메일 중복 검사
    exist_user = db.scalar(
        select(Users).where(Users.email == User_data.email)
    )

    if exist_user is not None:
        return HTTPException(
            status_code = 409,
            detail = "이미 사용중인 이메일입니다."
        )

    #비번 해싱
    hashed = password_hashing.hash(User_data.password)

    #User 객체 생성
    new_user = Users(
        email = User_data.email,
        password_hash = hashed,
        name = User_data.name,
        number = User_data.number
    )

    #User 객체 저장
    db.add(new_user)
    db.commit()

    return{
		 "success": True,
		 "message": "회원가입이 완료되었습니다."
    }