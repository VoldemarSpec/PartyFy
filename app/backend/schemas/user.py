from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    username: str       
    email: EmailStr
    id: int