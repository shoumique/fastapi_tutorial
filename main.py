from fastapi import FastAPI
from routers import post, user, auth, post_ai
import models
from database import engine

app = FastAPI()

app.include_router(post.router)
app.include_router(post_ai.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


models.Base.metadata.create_all(bind=engine)
