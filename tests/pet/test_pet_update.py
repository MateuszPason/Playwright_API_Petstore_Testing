from tests.payloads.pet_payloads import CREATE_PET, UPDATE_PET
from src.pet_utils import Pet
import pytest


@pytest.mark.smoke
def test_successful_pet_update(pet: Pet, init_pet, generate_pet_id):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)
    UPDATE_PET.id = pet_id

    update_response = pet.update_pet(data=UPDATE_PET.__dict__)
    update_response_body = update_response.json()

    assert update_response_body["id"] == pet_id
    assert update_response_body["category"] == UPDATE_PET.category
    assert update_response_body["name"] == UPDATE_PET.name
    assert update_response_body["photoUrls"] == UPDATE_PET.photoUrls
    assert update_response_body["tags"] == UPDATE_PET.tags
    assert update_response_body["status"] == UPDATE_PET.status

@pytest.mark.regression
def test_invalid_type_data_field(pet: Pet, init_pet, generate_pet_id):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)
    UPDATE_PET.id = pet_id
    UPDATE_PET.photoUrls = (
        ""  # Passing invalid data type | Expected: list of string | Actual: string
    )
    response = pet.update_pet(data=UPDATE_PET.__dict__)

    assert response.status == 500
