from tests.payloads.pet_payloads import CREATE_PET
from playwright.sync_api import APIRequestContext
from src.pet_utils import Pet

def test_delete_existing_pet(api_request_context: APIRequestContext,init_pet, generate_pet_id):
    pet_id = generate_pet_id
    CREATE_PET.id = pet_id
    created_pet = init_pet(CREATE_PET)

    assert created_pet['id'] == pet_id

    pet = Pet(api_request_context)
    response = pet.delete_pet(f'/v2/pet/{pet_id}')
    response_body = response.json()

    assert response.ok
    assert response_body['message'] == str(pet_id)

def test_delete_not_existing_pet(api_request_context: APIRequestContext, pet: Pet, generate_pet_id):
    pet_id = generate_pet_id
    pet = Pet(api_request_context)

    get_response = pet.get_pet(f'v2/pet/{pet_id}')

    if get_response.status != 404:
        pet.delete_pet(f'v2/pet/{pet_id}')

    delete_response = pet.delete_pet(f'v2/pet/{pet_id}')

    assert delete_response.status == 404