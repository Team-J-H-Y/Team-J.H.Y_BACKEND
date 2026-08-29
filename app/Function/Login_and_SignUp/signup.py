from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db
from database.Schemas.signup_schema import SignupData
from database.models.users import Users

#--------------------------------
#API 호출
app = FastAPI()

#라우터 연결
router_signup = APIRouter()

#회원가입 API
@router_signup.post("/api/users/signup")
def signup(User_data: SignupData, db: Session = Depends(Create_db)):
    #이메일 중복 확인
    existing_user = db.scalar(select(User).where(User.email == User_data.email))