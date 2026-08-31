from fastapi import FastAPI

from app.Function.Dev.Com_dev import router_dev
from app.Function.Login_and_SignUp.login import router_login
from app.Function.Login_and_SignUp.signup import router_signup
from app.Function.load_state.load_state import router_load_state
#--------------------------------
#API 호출
app = FastAPI()

#기능 api 호출
app.include_router(router_dev)
app.include_router(router_login)
app.include_router(router_signup)
app.include_router(router_load_state)