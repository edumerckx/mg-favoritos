from pydantic import BaseModel, EmailStr, Field


class CustomerSchema(BaseModel):
    name: str = Field(max_length=40)
    email: EmailStr
    password: str


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
