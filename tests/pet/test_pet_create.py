from playwright.sync_api import APIRequestContext
from src.pet_utils import Pet
from tests.payloads.pet_payloads import CREATE_PET
import uuid



def test_add_a_new_pet_to_the_store_returns_200(api_request_context: APIRequestContext):
    pet = Pet(api_request_context)
    pet_id = int(uuid.uuid4().int % 10000)
    CREATE_PET.id = pet_id
    response = pet.create_pet(
        "/v2/pet",
        data=CREATE_PET.__dict__
    )

    assert response.ok

    response_body = response.json()
    assert response_body["id"] == CREATE_PET.id
    assert response_body["name"] == CREATE_PET.name


def test_add_a_new_pet_to_the_store_wrong_method_used(api_request_context: APIRequestContext):
    pet = Pet(api_request_context)
    response = pet.get_pet("/v2/pet", data={})

    assert response.status == 405