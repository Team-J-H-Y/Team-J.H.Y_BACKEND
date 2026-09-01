from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db
from Schemas.signup_schema import SignupData
from models.users import Users

#--------------------------------

#라우터 연결
router_signup = APIRouter()

#회원가입 API
@router_signup.post("/api/users/signup")
def signup(User_data: SignupData, db: Session = Depends(Create_db)):



    pass