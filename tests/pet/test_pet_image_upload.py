from src.pet_utils import Pet
from tests.payloads.pet_payloads import CREATE_PET
import pytest

@pytest.mark.regression
@pytest.mark.parametrize(
        "file_name",
        ["solid_blue.jpg", "solid_blue.png"]
)
def test_successful_image_upload(pet: Pet, generate_pet_id, init_pet, file_name, pet_cleanup):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)

    image_path = f"tests/assets/images/{file_name}"  
    upload_response = pet.upload_image(f"/v2/pet/{pet_id}/uploadImage", image_path, "TestAdditionalData")

    assert upload_response.ok

    pet_cleanup(pet_id)

    # At the time of writing this test, pet object didn't return image file. 

@pytest.mark.regression
def test_no_image_file(pet: Pet, generate_pet_id, init_pet, pet_cleanup):
    pet_id = generate_pet_id()
    CREATE_PET.id = pet_id
    init_pet(CREATE_PET)

    update_response = pet.upload_image(f"/v2/pet/{pet_id}/uploadImage")

    assert update_response.status == 415

    pet_cleanup(pet_id)