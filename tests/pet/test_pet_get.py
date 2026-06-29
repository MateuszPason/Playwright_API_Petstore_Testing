from src.pet_utils import Pet
import pytest
from src.models.pet_models import PetResponse

@pytest.mark.smoke
def test_get_existing_pet(pet: Pet, init_pet, generate_id, pet_cleanup, new_pet):
    pet_id = generate_id()
    new_pet.id = pet_id
    init_pet(new_pet)

    response = pet.get_pet(pet_id)
    pet_data = PetResponse.model_validate(response.json())

    assert response.ok
    assert pet_data.id == pet_id
    assert pet_data.category == new_pet.category
    assert pet_data.name == new_pet.name
    assert pet_data.photoUrls == new_pet.photoUrls
    assert pet_data.tags == new_pet.tags
    assert pet_data.status == new_pet.status

    pet_cleanup(pet_id)

@pytest.mark.regression
def test_get_not_existing_pet(pet: Pet, generate_id, pet_cleanup):
    pet_id = generate_id()
    pet_cleanup(pet_id)

    response = pet.get_pet(pet_id)
    response_body = response.json()

    assert response.status == 404
    assert response_body["message"] == "Pet not found"

@pytest.mark.parametrize("incorrect_pet_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_pet_id(pet: Pet, incorrect_pet_id):
    with pytest.raises(ValueError, match="Incorrect pet_id"):
        pet.get_pet(incorrect_pet_id)
