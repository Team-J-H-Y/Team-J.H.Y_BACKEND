from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db

from database.models.state import State
from database.Schemas.schema import Device_State
from database.models.state_log import State_log
#--------------------------------
#API 호출
app = FastAPI()

#라우터 연결
router_dev = APIRouter()

#건조기 상태 변화 업데이트
@router_dev.patch("/api/state/{device_id}")
def update_state(device_id: str, state_data: Device_State, db: Session = Depends(Create_db)):

    #검증 코드 추가 필요


    #기존 데이터 가져오기
    update_state = db.get(State, device_id)

    #기존 데이터 업데이트
    update_state.state = state_data.state
    update_state.updated_at = datetime.now()
    db.commit()
    
    #상태 로그 추가
    create_log = State_log(
        device_id=update_state.device_id,
        state=update_state.state,
        created_at=update_state.updated_at
    )
    db.add(create_log)
    db.commit()

    return {
  "success": True,
  "message": "Success data",
  "data": {
		"deviceID": update_state.device_id,
		"state": update_state.state,
		"Vibration": state_data.Vibration,
		"V_Data_before": state_data.V_data_before,
		"V_Data_After": state_data.V_data_after,
		"Current": state_data.Current,
		"C_Data": state_data.C_data
	}
}