from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_zero.models import ToDoState


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


class FilterPageSchema(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(gt=0, default=10)


class FilterToDoSchema(FilterPageSchema):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = None
    state: ToDoState | None = None


class ToDoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    state: ToDoState | None = None


class ToDoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState = Field(default=ToDoState.todo)


class ToDoPublicSchema(ToDoSchema):
    id: int


class ToDoListSchema(BaseModel):
    todos: list[ToDoPublicSchema]
