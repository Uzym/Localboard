import os
import models
import schemas

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def ggame():
    return {"1": "2"}


@app.post("/add_user")
def add_user(user: schemas.User):
    db_user = models.User(name=user.name, chat_id=user.chat_id,
                          desc=user.desc, type=user.type)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get("/users")
def get_users():
    users = db.session.query(models.User).all()
    return users
