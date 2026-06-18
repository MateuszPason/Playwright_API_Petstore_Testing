from dataclasses import dataclass

@dataclass
class PetPayload:
    id: int
    category: dict
    name: str
    photoUrls: list
    tags: list
    status: str


CREATE_PET = PetPayload(
    id=None,
    category={"id": 101, "name": "TestingPet"},
    name="TestingPet101",
    photoUrls=[""],
    tags=[{"id": 101, "name": "101Pet"}],
    status="available",
)

UPDATE_PET = PetPayload(
    id=None,
    category={"id": 102, "name": "TestingPet - Updated"},
    name="TestingPet101 - Updated",
    photoUrls=["https://testphoto.jpg"],
    tags=[{"id": 102, "name": "101Pet - Updated"}],
    status="available - Updated",
)