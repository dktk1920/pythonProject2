from pydantic import BaseModel, EmailStr
from datetime import date

# 회원가입용 스키마
class UserCreate(BaseModel):
    userId: str
    name: str
    password: str
    email: EmailStr
    birthDate: date
    gender: str  # "male" 또는 "female"

# 로그인 요청 스키마
class UserLogin(BaseModel):
    userId: str
    password: str

# 로그인 응답 스키마
class UserLoginResponse(BaseModel):
    name: str
    userId: str
    loginMethod: str
    isAnonymous: bool
