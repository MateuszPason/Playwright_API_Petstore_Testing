from src.pet_utils import Pet
import pytest
from src.models.pet_models import PetResponse


@pytest.mark.regression
def test_pet_lifecycle(pet: Pet, generate_pet_id, new_pet, updated_pet):
    pet_id = generate_pet_id()
    new_pet.id = pet_id
    updated_pet.id = pet_id

    # Remove pet with generated pet_id - Make sure it doesn't exist before create/update
    pet.delete_pet(pet_id)

    response_create_pet = pet.create_pet(data=new_pet.model_dump())
    pet_data_create = PetResponse.model_validate(response_create_pet.json())
    assert pet_data_create.id == pet_id

    response_update_pet = pet.update_pet(data=updated_pet.model_dump())
    pet_data_update = PetResponse.model_validate(response_update_pet.json())
    assert pet_data_update.id == pet_id
    assert pet_data_update.category == updated_pet.category
    assert pet_data_update.name == updated_pet.name
    assert pet_data_update.photoUrls == updated_pet.photoUrls
    assert pet_data_update.tags == updated_pet.tags
    assert pet_data_update.status == updated_pet.status

    response_delete_pet = pet.delete_pet(pet_id)
    assert response_delete_pet.ok

    # Get pet with pet_id to check if it doesn't exist

    tested_pet = pet.get_pet(pet_id)
    tested_pet_body = tested_pet.json()
    assert tested_pet.status == 404
    assert tested_pet_body["message"] == "Pet not found"
