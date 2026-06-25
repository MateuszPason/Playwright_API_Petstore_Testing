from tests.payloads.pet_payloads import CREATE_PET
from src.pet_utils import Pet
import pytest

@pytest.mark.smoke
def test_get_existing_pet(pet: Pet, init_pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)

    response = pet.get_pet(pet_id)
    response_body = response.json()

    assert response.ok
    assert response_body["id"] == pet_id
    assert response_body["category"] == CREATE_PET.category
    assert response_body["name"] == CREATE_PET.name
    assert response_body["photoUrls"] == CREATE_PET.photoUrls
    assert response_body["tags"] == CREATE_PET.tags
    assert response_body["status"] == CREATE_PET.status

    pet_cleanup(pet_id)

@pytest.mark.regression
def test_get_not_existing_pet(pet: Pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id()
    pet_cleanup(pet_id)

    response = pet.get_pet(pet_id)
    response_body = response.json()

    assert response.status == 404
    assert response_body["message"] == "Pet not found"

@pytest.mark.parametrize("incorrect_pet_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_pet_id(pet: Pet, incorrect_pet_id):
    with pytest.raises(ValueError, match="Incorrect pet_id"):
        pet.get_pet(incorrect_pet_id)
