import os
import models
import schemas

from random import randint

from fastapi import FastAPI, Request, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# main

@app.get("/")
async def test():
    return {"1": "2"}

# locations

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


@app.post("/locations/add")
async def add_location(location: schemas.Location):
    db_location = models.Location(title=location.title)
    db.session.add(db_location)
    db.session.commit()
    return db_location


@app.delete("/locations/delete/{id}")
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

# user

@app.get("/users")
async def get_users():
    users = db.session.query(models.User).all()
    return users

def add_user_func(user: schemas.User):
    db_user = models.User(name="user"+str(randint(0,100000)), chat_id=user.chat_id)
    db.session.add(db_user)
    db.session.commit()
    return db_user

@app.post("/users/add")
async def add_user(user: schemas.User):
    return add_user_func(user)

@app.get("/users/get/{chat_id}")
async def get_user(chat_id: str, response: Response):
    return is_user(chat_id, response)

def is_user(chat_id: str, response: Response):
    try:
        user = db.session.query(models.User).filter_by(chat_id=chat_id).first()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "ans": 0,
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    if user != None:
        return {
            "ans": 1,
            "user": user
        }
    else:
        return {
            "ans": 0
        }

# offers

@app.get("/offers")
async def get_offers():
    offers = db.session.query(models.Offer).all()
    return offers

@app.post("/offers/add/")
async def add_offer(offer: schemas.OfferNew):

    user = is_user(chat_id=offer.chat_id, response=Response())
    user_id = 0
    if user["ans"] == 0:
        new_user = schemas.User(chat_id=offer.chat_id)
        db_user = add_user_func(new_user)
        user_id = db_user.user_id
    else:
        user_id = user["user"].user_id
    
    db_offer = models.Offer(
        user_id=user_id,
        hidden=1
    )
    db.session.add(db_offer)
    db.session.commit()

    return db_offer

@app.post("/offers/add/title")
async def add_offer_title(offer: schemas.OfferTitle):
    try:
        db.session.query(models.Offer).filter_by(offer_id=offer.offer_id).update({'title': offer.title})
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }

@app.post("/offers/add/desc")
async def add_offer_desc(offer: schemas.OfferDesc):
    try:
        db.session.query(models.Offer).filter_by(offer_id=offer.offer_id).update({'desc': offer.desc})
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }

@app.post("/offers/add/cost")
async def add_offer_cost(offer: schemas.OfferCost):
    try:
        db.session.query(models.Offer).filter_by(offer_id=offer.offer_id).update({'cost': offer.cost})
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }

@app.post("/offers/add/hidden")
async def add_offer_hidden(offer: schemas.OfferHidden):
    try:
        db.session.query(models.Offer).filter_by(
            offer_id=offer.offer_id
        ).update({
            'hidden': int(offer.hidden)
        })
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }

@app.get("/offers/get/{offer_id}")
async def get_offer(offer_id: int, response: Response):
    try:
        offer = db.session.query(models.Offer).filter_by(offer_id=offer_id).first()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return offer


# всю инфу по оферу и юзеру. OfferID -> userId -> 2 таблицы
# добавить группу chatID -> isSailer() -> userID -> таблица
# открыть / закрыть группу (PATCH на поле busy)
# userID -> ВСЕ открытые группы (принадлежащие юзеру)
#
