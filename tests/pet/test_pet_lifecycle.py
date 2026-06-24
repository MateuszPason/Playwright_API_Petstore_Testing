from src.pet_utils import Pet
from payloads.pet_payloads import CREATE_PET, UPDATE_PET


# @pytest.mark.regression
def test_petet_lifecycle(pet: Pet, generate_pet_id):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    UPDATE_PET.id = pet_id

    # Remove pet with generated pet_id - Make sure it doesn't exist before create/update
    pet.delete_pet(pet_id)

    response_create_pet = pet.create_pet(data=CREATE_PET.__dict__)
    response_create_pet_body = response_create_pet.json()
    assert "id" in response_create_pet_body
    assert response_create_pet_body["id"] == pet_id

    response_update_pet = pet.update_pet(data=UPDATE_PET.__dict__)
    response_update_pet_body = response_update_pet.json()
    assert "id" in response_update_pet_body
    assert response_update_pet_body["id"] == pet_id
    assert response_update_pet_body["category"] == UPDATE_PET.category
    assert response_update_pet_body["name"] == UPDATE_PET.name
    assert response_update_pet_body["photoUrls"] == UPDATE_PET.photoUrls
    assert response_update_pet_body["tags"] == UPDATE_PET.tags
    assert response_update_pet_body["status"] == UPDATE_PET.status

    response_delete_pet = pet.delete_pet(pet_id)
    assert response_delete_pet.ok

    # Get pet with pet_id to check if it doesn't exist

    tested_pet = pet.get_pet(pet_id)
    tested_pet_body = tested_pet.json()
    assert tested_pet.status == 404
    assert tested_pet_body["message"] == "Pet not found"
