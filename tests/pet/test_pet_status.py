from src.pet_utils import Pet
from tests.payloads.pet_payloads import CREATE_PET
import pytest


@pytest.mark.regression
@pytest.mark.parametrize(
        "status",
        ["available", "pending", "sold"]
)
def test_correct_status(pet: Pet, init_pet, generate_pet_id, pet_cleanup, status):
    
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    CREATE_PET.status = status
    init_pet(CREATE_PET)

    available_pets = pet.get_pet_by_status(status)
    available_pets_body = available_pets.json()

    pet_to_assert = next((pet for pet in available_pets_body if pet.get("id") == pet_id), None)

    assert available_pets.ok
    assert pet_to_assert["status"] == status

    pet_cleanup(pet_id)

@pytest.mark.regression
@pytest.mark.parametrize(
        "status",
        [None, "Not existing status"]
)
def test_invalid_status(pet: Pet, status):
    response = pet.get_pet_by_status(status)
    response_body = response.json()

    assert response.ok
    assert response_body == []