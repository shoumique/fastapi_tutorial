from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor

import time
from sqlalchemy.orm import Session

import models
from database import engine, get_db
import schemas
import utils
from routers import post, user, auth


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
