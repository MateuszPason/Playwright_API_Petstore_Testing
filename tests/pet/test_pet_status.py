from src.pet_utils import Pet
import pytest
from src.models.pet_models import PetResponse


@pytest.mark.regression
@pytest.mark.parametrize(
        "status",
        ["available", "pending", "sold"]
)
def test_correct_status(pet: Pet, init_pet, generate_pet_id, pet_cleanup, status, new_pet):
    
    pet_id = generate_pet_id()
    new_pet.id = pet_id
    new_pet.status = status
    init_pet(new_pet)

    available_pets = pet.get_pet_by_status(status)
    available_pets_body = available_pets.json()

    pet_to_assert = PetResponse.model_validate(next((pet for pet in available_pets_body if pet.get("id") == pet_id), None))

    assert available_pets.ok
    assert pet_to_assert.status == status

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