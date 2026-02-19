from pydantic import BaseModel, validator
import re


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
