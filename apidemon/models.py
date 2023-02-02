from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(Integer, unique=True)
    desc = Column(String)
    type = Column(String)

    groups = relationship("Groups", back_populates="user")
    request_log = relationship("RequestLog", back_populates="user")
    offer = relationship("Offer", back_populates="user")


class Groups(Base):

    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True)
    busy = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.user_id"))

    user = relationship("User", back_populates="groups")
    request = relationship("Request", back_populates="groups")


class Request(Base):

    __tablename__ = "request"

    request_id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offer.offer_id"))
    user_id = Column(Integer, unique=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"))

    offer = relationship("Offer", back_populates="request")
    groups = relationship("Groups", back_populates="request")


class RequestLog(Base):

    __tablename__ = "request_log"

    request_log_id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("user.user_id"))
    customer_id = Column(Integer, ForeignKey("user.user_id"))
    info = Column(String)
    time = Column(DateTime)

    user = relationship("User", back_populates="request_log")


class Offer(Base):

    __tablename__ = "offer"

    offer_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cost = Column(Numeric)
    tag = Column(String)
    desc = Column(String)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    hidden = Column(Integer)
    location_id = Column(Integer, ForeignKey("location.location_id"))

    user = relationship("User", back_populates="offer")
    location = relationship("Location", back_populates="offer")
    offer_photo = relationship("OfferPhoto", back_populates="offer")


class OfferPhoto(Base):

    __tablename__ = "offer_photo"

    offer_photo_id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offer.offer_id"))
    photo_url = Column(String, unique=True)

    offer = relationship("Offer", back_populates="offeer_photo")


class Location(Base):

    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    offer = relationship("Offer", back_populates="location")
