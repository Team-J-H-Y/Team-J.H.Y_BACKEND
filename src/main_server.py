from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db
from database.models.state import State
from database.Schemas.schema import Device_State
#--------------------------------
#API 호출
app = FastAPI()

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

#건조기 상태 변화 업데이트
@app.put("/api/state/{device_id}")
def update_state(device_id: str, state_data: Device_State, db: Session = Depends(Create_db)):

    #검증 코드 추가 필요


    #판단 결과로 state를 업데이트
    update_state = db.get(State, device_id)

    

    db.add(new_state)
    db.commit()
    db.refresh(new_state)

    return {
  "success": True,
  "message": "Success data",
  "data": {
		"deviceID": new_state.device_id,
		"state": new_state.state,
		"Vibration": new_state.vibration,
		"V_Data_before": new_state.v_data_before,
		"V_Data_After": new_state.v_data_after,
		"Current": new_state.current,
		"C_Data": new_state.c_data
	}
}

