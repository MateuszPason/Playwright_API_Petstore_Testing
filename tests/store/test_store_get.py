from src.store_utils import Store
from tests.payloads.pet_payloads import CREATE_PET
from copy import deepcopy
import pytest

@pytest.mark.smoke
def test_existing_status(
    store: Store, generate_pet_id, generate_random_string, init_pet, pet_cleanup
):
    pet_id = generate_pet_id()
    pet_status = generate_random_string()

    CREATE_PET.id = pet_id
    CREATE_PET.status = pet_status

    init_pet(CREATE_PET)

    store_response = store.get_pet_inventories_in_store()
    store_response_body = store_response.json()

    assert store_response.ok
    assert store_response_body[pet_status] == 1

    pet_cleanup(pet_id)

@pytest.mark.regression
def test_non_existing_status(store: Store, generate_random_string):
    non_existing_status = generate_random_string()

    store_response = store.get_pet_inventories_in_store()
    store_response_body = store_response.json()

    assert store_response.ok
    assert non_existing_status not in store_response_body


@pytest.mark.regression
def test_accumulate_pets_with_same_status(
    store: Store, init_pet, pet_cleanup, generate_pet_id, generate_random_string
):
    pet_id_one = generate_pet_id()
    pet_id_two = generate_pet_id()
    pet_status = generate_random_string()

    pet_payload_1 = deepcopy(CREATE_PET)
    pet_payload_1.id = pet_id_one
    pet_payload_1.status = pet_status
    pet_payload_2 = deepcopy(CREATE_PET)
    pet_payload_2.id = pet_id_two
    pet_payload_2.status = pet_status

    init_pet(pet_payload_1)
    init_pet(pet_payload_2)

    store_response = store.get_pet_inventories_in_store()
    store_response_body = store_response.json()

    assert store_response_body[pet_status] == 2

    pet_cleanup(pet_id_one)
    pet_cleanup(pet_id_two)

@pytest.mark.smoke
def test_response_structure(store: Store):
    store_response = store.get_pet_inventories_in_store()
    store_response_body = store_response.json()

    assert type(store_response_body) is dict
    assert all(isinstance(key, str) for key in store_response_body)
    assert all(isinstance(value, int) for value in store_response_body.values())
    assert all([0 < value for value in store_response_body.values()])

@pytest.mark.regression
def test_consistent_response(
    store: Store, init_pet, pet_cleanup, generate_pet_id, generate_random_string
):
    pet_id = generate_pet_id()
    unique_status = generate_random_string()

    pet_payload = deepcopy(CREATE_PET)
    pet_payload.id = pet_id
    pet_payload.status = unique_status

    init_pet(pet_payload)

    first_store_response_body = store.get_pet_inventories_in_store().json()
    second_store_response_body = store.get_pet_inventories_in_store().json()

    assert first_store_response_body.get(unique_status) == 1
    assert second_store_response_body.get(unique_status) == 1

    pet_cleanup(pet_id)