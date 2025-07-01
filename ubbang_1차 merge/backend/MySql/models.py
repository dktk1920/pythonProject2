from sqlalchemy import Column, String, Date
from .database import Base

class User(Base):
    __tablename__ = "users"

    userId = Column(String(100), primary_key=True, index=True)  # PK + index
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt 해시 저장을 위한 충분한 길이 확보
    email = Column(String(100), nullable=False, unique=True)    # 이메일도 유일하게 설정하면 좋아
    gender = Column(String(10), nullable=True)  # male / female
    birthDate = Column(Date, nullable=True)
