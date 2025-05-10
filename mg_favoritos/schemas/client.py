from pydantic import BaseModel, EmailStr, Field


class ClientSchema(BaseModel):
    name: str = Field(max_length=40)
    email: EmailStr
    password: str


class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
