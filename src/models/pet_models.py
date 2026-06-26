from pydantic import BaseModel

class Category(BaseModel):
    id: int | None
    name: str | None

class Tag(BaseModel):
    id: int | None
    name: str | None

class PetPayload(BaseModel):
    id: int | None = None
    category: Category | None = None
    name: str
    photoUrls: list
    tags: list[Tag] | None = None
    status: str | None = None

class PetResponse(BaseModel):
    id: int | None
    category: Category | None
    name: str
    photoUrls: list[str]
    tags: list[Tag] | None
    status: str | None