from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile


class User(BaseModel):

    chat_id: str

    class Config:
        orm_mode = True

class OfferNew(BaseModel):

    chat_id: str
    class Config:
        orm_mode = True

class OfferTitle(BaseModel):

    offer_id: int
    title: str

    class Config:
        orm_mode = True

class OfferCost(BaseModel):

    offer_id: int
    cost: int

    class Config:
        orm_mode = True

class OfferDesc(BaseModel):

    offer_id: int
    desc: str

    class Config:
        orm_mode = True

class OfferHidden(BaseModel):

    offer_id: int
    hidden: bool

    class Config:
        orm_mode = True

class OfferQuantity(BaseModel):

    offer_id: int
    quantity: int

    class Config:
        orm_mode = True

class OfferCanGroup(BaseModel):

    offer_id: int
    can_add_in_group: bool
    

class OfferList(BaseModel):
    use_chat_id: bool
    chat_id: str
    use_hidden: bool
    list_start: int
    list_end: int

    class Config:
        orm_mode = True

class Offer(BaseModel):

    title: str
    cost: str
    tag: str
    desc: str
    user_id: int
    location_id: int

    class Config:
        orm_mode = True


class OfferPhoto(BaseModel):

    offer_id: int
    photo: str

    class Config:
        orm_mode = True
