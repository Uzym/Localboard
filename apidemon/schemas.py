from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):

    name: str
    chat_id: int
    desc: str
    type: str

    class Config:
        orm_mode = True


class Groups(BaseModel):

    chat_id: int
    busy: int

    class Config:
        orm_mode = True


class newOffer(BaseModel):

    chat_id: int
    title: str
    cost: str
    tag: str
    desc: str
    location_id: int
    hidden: int

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