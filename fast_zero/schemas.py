from pydantic import BaseModel, ConfigDict, EmailStr


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
