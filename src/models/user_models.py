from pydantic import BaseModel

class UserPayload(BaseModel):
    id: int | None
    username: str | None
    firstName: str | None
    lastName: str | None
    email: str | None
    password: str | None
    phone: str | None
    userStatus: int | None

class UserResponse(BaseModel):
    id: int | None
    username: str | None
    firstName: str | None
    lastName: str | None
    email: str | None
    password: str | None
    phone: str | None
    userStatus: int | None