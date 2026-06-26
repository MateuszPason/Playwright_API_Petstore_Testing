from src.pet_utils import Pet
import pytest
from src.models.pet_models import PetResponse

@pytest.mark.smoke
def test_add_a_new_pet_to_the_store_returns_200(pet: Pet, generate_pet_id, pet_cleanup, new_pet):
    pet_id = generate_pet_id()
    new_pet.id = pet_id
    response = pet.create_pet(data=new_pet.model_dump())

    assert response.ok

    pet_data = PetResponse.model_validate(response.json())
    assert pet_data.id == new_pet.id
    assert pet_data.name == new_pet.name

    pet_cleanup(pet_id)