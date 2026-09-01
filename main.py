from fastapi import FastAPI

from api.v1.endpoints.update_state import router_dev
from api.v1.endpoints.login import router_login
from api.v1.endpoints.signup import router_signup
from api.v1.endpoints.load_state import router_load_state
#--------------------------------
#API 호출
app = FastAPI()

#기능 api 호출
app.include_router(router_dev)
app.include_router(router_login)
app.include_router(router_signup)
app.include_router(router_load_state)