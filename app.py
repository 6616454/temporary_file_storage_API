from fastapi import FastAPI
from do_rar import router as rar_router
from auth.api import router as auth_router

app = FastAPI()

app.include_router(rar_router)
app.include_router(auth_router)
