from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(Integer, unique=True)
    desc = Column(String)
    type = Column(String)


class Groups(Base):

    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True)
    busy = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.user_id"))

    owner = relationship("User", foreign_keys=[owner_id])


class Request(Base):

    __tablename__ = "request"

    request_id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offer.offer_id"))
    user_id = Column(Integer, unique=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"))

    offer = relationship("Offer", foreign_keys=[offer_id])
    offer = relationship("Groups", foreign_keys=[group_id])


class RequestLog(Base):

    __tablename__ = "request_log"

    request_log_id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("user.user_id"))
    customer_id = Column(Integer, ForeignKey("user.user_id"))
    info = Column(String)
    time = Column(DateTime)

    provider = relationship("User", foreign_keys=[provider_id])
    customer = relationship("User", foreign_keys=[customer_id])


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

    user = relationship("User", foreign_keys=[user_id])
    location = relationship("Location", foreign_keys=[location_id])


class OfferPhoto(Base):

    __tablename__ = "offer_photo"

    offer_photo_id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offer.offer_id"))
    photo_url = Column(String, unique=True)

    offer = relationship("Offer", foreign_keys=[offer_id])


class Location(Base):

    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)