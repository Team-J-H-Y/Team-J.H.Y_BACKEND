from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db

from app.Function.Dev.Com_dev import router_dev
from app.Function.Login_and_SignUp.login import router_login
from app.Function.Login_and_SignUp.signup import router_signup

from database.models.state import State
from database.models.devices import Devices

from database.base import Base
#--------------------------------
#API 호출
app = FastAPI()

#기능 api 호출
app.include_router(router_dev)
app.include_router(router_login)
app.include_router(router_signup)

print(Base.metadata.tables.keys())
print(State.__table__.metadata is Devices.__table__.metadata)

#메인 화면 호출
@app.get("/")
def main():
    return "message"

#건조기 테이블 조회
@app.get("/api/state/all")
def get_states(db: Session = Depends(Create_db)):
    stmt = select(State)
    state = db.scalar(stmt).all()

    return state

#개별 건조기 테이블 조회
@app.get("/api/state/{device_id}")
def get_states(device_id: int, db: Session = Depends(Create_db)):
    stmt = select(State, device_id)
    state = db.scalar(stmt)

    return state
