from pydantic import BaseModel

#센서값 스키마
class Device_State(BaseModel):
    device_id: str
    state: str
    Vibration: bool
    V_data_before: list
    V_data_after: list
    Current: bool
    C_data: str

