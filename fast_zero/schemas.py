from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class PublicUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserListSchema(BaseModel):
    users: list[PublicUserSchema]


class TokenSchema(BaseModel):
    token_type: str
    access_token: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(gt=0, default=10)
