#----------모듈 불러오기----------
from fastapi import Depends, APIRouter
from database.connection import Create_db
from sqlalchemy import select
from sqlalchemy.orm import Session

#파일 연결
from database.models.state import State
#----------라우터 연결----------
router_load_state = APIRouter()


#건조기 테이블 조회
@router_load_state.get("/api/state/all")
def get_states(db: Session = Depends(Create_db)):
    stmt = select(State)
    state = db.scalar(stmt).all()

    return state

#개별 건조기 테이블 조회
@router_load_state.get("/api/state/{device_id}")
def get_states(device_id: str, db: Session = Depends(Create_db)):
    stmt = select(State, device_id)
    state = db.scalar(stmt)

    return state
