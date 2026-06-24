from tests.payloads.pet_payloads import CREATE_PET
from src.pet_utils import Pet


def test_add_a_new_pet_to_the_store_returns_200(pet: Pet, generate_pet_id, pet_cleanup):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    response = pet.create_pet(data=CREATE_PET.__dict__)

    assert response.ok

    response_body = response.json()
    assert response_body["id"] == CREATE_PET.id
    assert response_body["name"] == CREATE_PET.name

    pet_cleanup(pet_id)