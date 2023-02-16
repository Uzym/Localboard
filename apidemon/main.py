import os
import models
import schemas

from fastapi import FastAPI, Request, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def ggame():
    return {"1": "2"}


@app.get("/locations")
async def get_locations(response: Response):
    try:
        locations = db.session.query(models.Location).first()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return locations


@app.post("/locations")
async def add_location(location: schemas.Location):
    db_location = models.Location(title=location.title)
    db.session.add(db_location)
    db.session.commit()
    return db_location


@app.delete("/locations/{id}")
async def delete_location(id: int, response: Response):
    try:
        location = db.session.query(
            models.Location).filter_by(location_id=id).delete()
        db.session.commit()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return location


@app.post("/users")
async def add_user(user: schemas.User):
    db_user = models.User(name=user.name, chat_id=user.chat_id,
                          desc=user.desc, type=user.type)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get("/users")
async def get_users():
    users = db.session.query(models.User).all()
    return users


@app.get("/is_user/{id}")
async def is_user(id: int):
    
    user = db.session.query(models.User).filter_by(chat_id=id).all()
    
    if len(user) == 0:
        return {"ans": "not found"}
    user_id = user[0].user_id
    return {"ans": "ok", "user_id": user_id}
        

@app.get("/users/{id}")
async def get_user(id: int, response: Response):
    try:
        user = db.session.query(models.User).filter_by(user_id=id).all()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return user


@app.get("/offers")
async def get_offers():
    offers = db.session.query(models.Offer).all()
    return offers


#@app.get("/add_desc_offer")

@app.get("/offers/{id}")
async def new_offer(id: int):
    user = await is_user(id)
        # if (user["ans"] == "ok"):
        #     new_offer = models.Offer(
        #         title=offer.title, cost=offer.cost, tag=offer.tag,
        #         desc=offer.desc, user_id=user["user"]["user_id"],
        #         location_id=offer.location_id, hidden=offer.hidden)
        #     db.session.add(new_offer)
        #     db.session.commit()
        # else:
        #     response.status_code = status.HTTP_400_BAD_REQUEST
        #     return {
        #         "error": "no sailer"
        #     }
    return user

# всю инфу по оферу и юзеру. OfferID -> userId -> 2 таблицы
# добавить группу chatID -> isSailer() -> userID -> таблица
# открыть / закрыть группу (PATCH на поле busy)
# userID -> ВСЕ открытые группы (принадлежащие юзеру)
#
