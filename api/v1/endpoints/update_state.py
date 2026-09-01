from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime

from database.connection import Create_db

from models.state import State
from Schemas.schema import Device_State
from models.state_log import State_log
from models.devices import Devices
#--------------------------------

#라우터 연결
router_dev = APIRouter()

#건조기 상태 변화 업데이트
@router_dev.patch("/api/state/{device_id}")
def update_state(device_id: str, state_data: Device_State, db: Session = Depends(Create_db)):

    now = datetime.now()

    #device_id 존재 여부 파악
    is_exist = db.get(Devices, device_id)
    
    if is_exist is None:
        return "Device_id is not exist."
    
    #검증 코드 추가 필요





    #--------검증 결과가 참일때 실행-------------------------------
    #기존 데이터 가져오기
    exist_state = db.get(State, device_id)

    #기존 데이터 존재여부 파악
    if exist_state is None:
        #새 데이터 추가
        app_new = State(
            device_id = state_data.device_id,
            state=state_data.state,
            updated_at = now
        )
        db.add(app_new)
        db.commit()



    else:
        #기존 데이터 수정
            

        #기존 데이터 업데이트
        exist_state.state = state_data.state
        exist_state.updated_at = now
        db.commit()
        
    #상태 로그 추가
    create_log = State_log(
    device_id=state_data.device_id,
    state=state_data.state,
    created_at=now
    )
    db.add(create_log)
    db.commit()

    return {
    "success": True,
    "message": "Success data",
    "data": {
            "deviceID": exist_state.device_id,
            "state": exist_state.state,
            "Vibration": state_data.Vibration,
            "V_Data_before": state_data.V_data_before,
            "V_Data_After": state_data.V_data_after,
            "Current": state_data.Current,
            "C_Data": state_data.C_data
        }
    }