from fastapi import FastAPI
from do_rar import router

app = FastAPI()

app.include_router(router)
