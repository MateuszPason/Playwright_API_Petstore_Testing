from src.store_utils import Store
import pytest

@pytest.mark.smoke
def test_get_an_existing_order(store: Store, generate_order_id, generate_pet_id, ship_date, create_order, order_cleanup):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    create_order(order_id, pet_id, 1, ship_date, "placed", True)

    returned_order = store.get_order_by_id(order_id)
    assert returned_order.ok

    returned_order_body = returned_order.json()
    assert returned_order_body["id"] == order_id
    assert returned_order_body["petId"] == pet_id
    assert returned_order_body["quantity"] == 1
    assert returned_order_body["shipDate"] == ship_date
    assert returned_order_body["status"] == "placed"
    assert returned_order_body["complete"] is True

    order_cleanup(order_id)

@pytest.mark.parametrize("incorrect_order_id", [0, -1, True, False, "123", None, 1.5])
def test_invalid_order_id(store: Store, incorrect_order_id):
    with pytest.raises(ValueError, match="Incorrect order_id"):
        store.get_order_by_id(incorrect_order_id)

@pytest.mark.regression
def test_get_non_existing_order(store: Store, generate_order_id, generate_pet_id, ship_date, create_order, order_cleanup):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    create_order(order_id, pet_id, 1, ship_date, "placed", True)
    order_cleanup(order_id)

    order_response = store.get_order_by_id(order_id)
    assert order_response.status == 404