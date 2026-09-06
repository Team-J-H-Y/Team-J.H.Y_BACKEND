from fastapi import FastAPI, Depends, APIRouter
#--------------------------------
#API 호출
app = FastAPI()

router_login = APIRouter()

@router_login.post("/api/v1/users/login")
def login():
    
    pass