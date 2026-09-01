from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from database.connection import Create_db

from models.state import State
from Schemas.schema import Device_State
#--------------------------------
#API 호출
app = FastAPI()

router_login = APIRouter()

@router_login.post("/api/users/login")
def login():
    pass