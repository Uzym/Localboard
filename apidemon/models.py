from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Продавец")
    chat_id = Column(String, unique=True, nullable=False)

class Offer(Base):

    __tablename__ = "offer"

    offer_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Товар")
    cost = Column(Integer, default=1)
    desc = Column(String, default="Описание")
    user_id = Column(Integer, ForeignKey("user.user_id"))
    hidden = Column(Integer, default=True)
    quantity = Column(Integer, default=1)
    can_add_in_group = Column(Boolean, default=False)
    photo = Column(String, default=None)

    user = relationship("User", foreign_keys=[user_id])
