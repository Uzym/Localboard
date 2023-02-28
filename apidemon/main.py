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
    db_user = models.User(
        name="user"+str(randint(0, 100000)), chat_id=user.chat_id)
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


@app.delete("/offers/delete/{id}")
async def delete_location(id: int, response: Response):
    try:
        location = db.session.query(
            models.Offer).filter_by(offer_id=id).delete()
        db.session.commit()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "ans": 0,
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return location


@app.post("/offers/get/list/")
async def get_list_offers(offer_list: schemas.OfferList):
    if offer_list.use_hidden:
        if offer_list.use_chat_id:
            try:
                user = is_user(chat_id=offer_list.chat_id, response=Response())
                if user["ans"] == 0:
                    return {"ans": 0}
                user_id = user["user"].user_id
                db_offer_list = db.session.query(models.Offer).filter_by(
                    user_id=user_id).limit(limit=offer_list.list_end).all()
                db_offer_list = db_offer_list[offer_list.list_start::]
                return {"offers": db_offer_list, "ans": 1}
            except Exception as e:
                return {"ans": 0, "error": e}
        else:
            try:
                db_offer_list = db.session.query(models.Offer).limit(
                    limit=offer_list.list_end).all()
                db_offer_list = db_offer_list[offer_list.list_start::]
                return {"ans": 1, "offers": db_offer_list}
            except Exception as e:
                return {"ans": 0, "error": e}
    else:
        if offer_list.use_chat_id:
            try:
                user = is_user(chat_id=offer_list.chat_id, response=Response())
                if user["ans"] == 0:
                    return {"ans": 0}
                user_id = user["user"].user_id
                db_offer_list = db.session.query(models.Offer).filter_by(
                    user_id=user_id, hidden=0).limit(limit=offer_list.list_end).all()
                db_offer_list = db_offer_list[offer_list.list_start::]
                return {"offers": db_offer_list, "ans": 1}
            except Exception as e:
                return {"ans": 0, "error": e}
        else:
            try:
                db_offer_list = db.session.query(models.Offer).filter_by(
                    hidden=0).limit(limit=offer_list.list_end).all()
                db_offer_list = db_offer_list[offer_list.list_start::]
                return {"ans": 1, "offers": db_offer_list}
            except Exception as e:
                return {"ans": 0, "error": e}


@app.get("/offers/get/my/{chat_id}")
async def get_my_offers(chat_id: str, response: Response):
    user = is_user(chat_id=chat_id, response=response)
    if user["ans"] == 0:
        return {"ans": 0}
    user_id = user["user"].user_id
    offers = db.session.query(models.Offer).filter_by(user_id=user_id).all()
    return {"offers": offers, "ans": 1}


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

    db_offer.user_id
    return {"offer": db_offer, "ans": 1}


@app.post("/offers/add/title")
async def add_offer_title(offer: schemas.OfferTitle):
    try:
        db.session.query(models.Offer).filter_by(
            offer_id=offer.offer_id).update({'title': offer.title})
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }


@app.post("/offers/add/desc")
async def add_offer_desc(offer: schemas.OfferDesc):
    try:
        db.session.query(models.Offer).filter_by(
            offer_id=offer.offer_id).update({'desc': offer.desc})
        db.session.commit()
        return {"ans": "ok"}
    except Exception as e:
        return {
            "error": e
        }


@app.post("/offers/add/cost")
async def add_offer_cost(offer: schemas.OfferCost):
    try:
        db.session.query(models.Offer).filter_by(
            offer_id=offer.offer_id).update({'cost': offer.cost})
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


@app.post("/offers/add/quantity")
async def add_offer_hidden(offer: schemas.OfferQuantity):
    try:
        db.session.query(models.Offer).filter_by(
            offer_id=offer.offer_id
        ).update({
            'quantity': int(offer.quantity)
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
        offer = db.session.query(models.Offer).filter_by(
            offer_id=offer_id).first()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "ans": 0,
            "error": e
        }
    response.status_code = status.HTTP_200_OK
    return {"offer": offer, "ans": 1}
