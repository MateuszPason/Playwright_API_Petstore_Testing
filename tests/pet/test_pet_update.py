from src.pet_utils import Pet
import pytest
from src.models.pet_models import PetResponse


@pytest.mark.smoke
def test_successful_pet_update(pet: Pet, init_pet, generate_pet_id, new_pet, updated_pet):
    pet_id = generate_pet_id()
    new_pet.id = pet_id
    init_pet(new_pet)
    updated_pet.id = pet_id

    update_response = pet.update_pet(data=updated_pet.model_dump())
    pet_data = PetResponse.model_validate(update_response.json())

    assert pet_data.id == pet_id
    assert pet_data.category == updated_pet.category
    assert pet_data.name == updated_pet.name
    assert pet_data.photoUrls == updated_pet.photoUrls
    assert pet_data.tags == updated_pet.tags
    assert pet_data.status == updated_pet.status