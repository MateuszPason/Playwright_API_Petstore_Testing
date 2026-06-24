from tests.payloads.pet_payloads import CREATE_PET
from src.pet_utils import Pet
import pytest


def test_delete_existing_pet(pet: Pet, init_pet, generate_pet_id):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    created_pet = init_pet(CREATE_PET)
    created_pet_body = created_pet.json()

    assert created_pet_body["id"] == pet_id

    response = pet.delete_pet(pet_id)
    response_body = response.json()

    assert response.ok
    assert response_body["message"] == str(pet_id)


def test_delete_not_existing_pet(pet: Pet, generate_pet_id):
    pet_id = generate_pet_id()

    get_response = pet.get_pet(pet_id)

    if get_response.status != 404:
        pet.delete_pet(pet_id)

    delete_response = pet.delete_pet(pet_id)

    assert delete_response.status == 404

@pytest.mark.parametrize("incorrect_pet_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_pet_id(pet: Pet, incorrect_pet_id):
    with pytest.raises(ValueError, match="Incorrect pet_id"):
        pet.delete_pet(incorrect_pet_id)