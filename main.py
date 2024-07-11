from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from db import init_db
import router
# Path to the service account key file
load_dotenv()

@asynccontextmanager
async def lifesapn(app: FastAPI):
    init_db()
    yield



app = FastAPI(lifespan=lifesapn)
app.include_router(router.user_router)




@app.get("/")
async def home():
    return {"message": "hello world"}