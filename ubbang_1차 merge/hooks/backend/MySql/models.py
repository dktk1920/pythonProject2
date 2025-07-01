from sqlalchemy import Column, String, Date, Text, Integer
from .database import Base

class User(Base):
    __tablename__ = "users"

    pk = Column(Integer, primary_key=True, index=True)
    userId = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    password = Column(String(255))
    email = Column(String(100))
    birthDate = Column(Date)
    gender = Column(String(10))
    socialId = Column(String(100))
    worry = Column(Text)
    mode = Column(String(20))
    age = Column(Integer)
