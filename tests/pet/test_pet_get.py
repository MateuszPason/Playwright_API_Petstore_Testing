from playwright.sync_api import APIRequestContext
from tests.payloads.pet_payloads import CREATE_PET
from src.pet_utils import Pet


def test_get_existing_pet(api_request_context: APIRequestContext, init_pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id
    CREATE_PET.id = generate_pet_id
    init_pet(CREATE_PET)

    pet = Pet(api_request_context)
    response = pet.get_pet(f'/v2/pet/{pet_id}')
    response_body = response.json()

    assert response.ok
    assert response_body['id'] == pet_id
    assert response_body['category'] == CREATE_PET.category
    assert response_body['name'] == CREATE_PET.name
    assert response_body['photoUrls'] == CREATE_PET.photoUrls
    assert response_body['tags'] == CREATE_PET.tags
    assert response_body['status'] == CREATE_PET.status

    pet_cleanup(pet_id)

def test_get_not_existing_pet(generate_pet_id, api_request_context: APIRequestContext, pet: Pet):
    pet_id = generate_pet_id
    pet = Pet(api_request_context)
    pet.delete_pet(f'/v2/pet/{pet_id}')

    response = pet.get_pet(f'v2/pet/{pet_id}')
    response_body = response.json()

    assert response.status == 404
    assert response_body['message'] == 'Pet not found'