from tests.payloads.pet_payloads import CREATE_PET
from src.pet_utils import Pet


def test_delete_existing_pet(pet: Pet, init_pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id
    CREATE_PET.id = pet_id
    created_pet = init_pet(CREATE_PET)
    created_pet_body = created_pet.json()

    assert created_pet_body["id"] == pet_id

    response = pet_cleanup(pet_id)
    response_body = response.json()

    assert response.ok
    assert response_body["message"] == str(pet_id)


def test_delete_not_existing_pet(pet: Pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id

    get_response = pet.get_pet(f"v2/pet/{pet_id}")

    if get_response.status != 404:
        pet_cleanup(pet_id)

    delete_response = pet_cleanup(pet_id)

    assert delete_response.status == 404
