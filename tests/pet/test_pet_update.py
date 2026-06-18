from tests.payloads.pet_payloads import CREATE_PET, UPDATE_PET
from src.pet_utils import Pet
from playwright.sync_api import APIRequestContext
import uuid


def test_succesful_pet_update(api_request_context: APIRequestContext, init_pet):
    pet_id = int(uuid.uuid4().int % 10000)
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)
    UPDATE_PET.id = pet_id

    pet = Pet(api_request_context)
    update_response = pet.update_pet('/v2/pet', data=UPDATE_PET.__dict__)
    update_response_body = update_response.json()

    assert update_response_body['id'] == pet_id
    assert update_response_body['category'] == UPDATE_PET.category
    assert update_response_body['name'] == UPDATE_PET.name
    assert update_response_body['photoUrls'] == UPDATE_PET.photoUrls
    assert update_response_body['tags'] == UPDATE_PET.tags
    assert update_response_body['status'] == UPDATE_PET.status

def test_invalid_type_data_field(api_request_context: APIRequestContext, init_pet):
    pet_id = int(uuid.uuid4().int % 10000)
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)
    UPDATE_PET.id = pet_id
    UPDATE_PET.photoUrls = "" # Passing invalid data type | Expected: list of string | Actual: string
    pet = Pet(api_request_context)
    response = pet.update_pet('/v2/pet', data=UPDATE_PET.__dict__)

    assert response.status == 500