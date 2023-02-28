from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):

    chat_id: str

    class Config:
        orm_mode = True


class Groups(BaseModel):

    chat_id: int
    busy: int

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
    cost: str

    class Config:
        orm_mode = True

class OfferTag(BaseModel):

    offer_id: int
    tag: str

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

    photo_url: str

    class Config:
        orm_mode = True


class Location(BaseModel):

    title: str

    class Config:
        orm_mode = True


class RequestLog(BaseModel):

    info: str
    time: datetime

    class Config:
        orm_mode = True


class Request(BaseModel):

    user_id: int

    class Config:
        orm_mode = True


class Reply(BaseModel):

    status: str
    message: str