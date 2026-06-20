from src.pet_utils import Pet
from tests.payloads.pet_payloads import CREATE_PET


def test_add_a_new_pet_to_the_store_returns_200(generate_pet_id, init_pet, pet_cleanup):
    pet_id = generate_pet_id
    CREATE_PET.id = pet_id
    response = init_pet(CREATE_PET)

    assert response.ok

    response_body = response.json()
    assert response_body["id"] == CREATE_PET.id
    assert response_body["name"] == CREATE_PET.name

    pet_cleanup(pet_id)


def test_add_a_new_pet_to_the_store_wrong_method_used(pet: Pet):
    response = pet.get_pet("/v2/pet", data={})

    assert response.status == 405
