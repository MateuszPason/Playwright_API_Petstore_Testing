from pydantic import BaseModel

class OrderResponse(BaseModel):
    id: int | None
    petId: int | None
    quantity: int | None
    shipDate: str | None
    status: str | None
    complete: bool | None