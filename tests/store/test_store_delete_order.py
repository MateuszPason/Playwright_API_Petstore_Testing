from src.store_utils import Store
import pytest

def test_successful_order_delete(store: Store, generate_order_id, generate_pet_id, ship_date, create_order):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    create_order(order_id, pet_id, 1, ship_date, "placed", False)

    removed_order = store.delete_an_order(order_id)
    assert removed_order.ok

    fetched_data_of_removed_order = store.get_order_by_id(order_id)
    assert fetched_data_of_removed_order.status == 404

@pytest.mark.parametrize("incorrect_order_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_order_id(store: Store, incorrect_order_id):
    with pytest.raises(ValueError, match="Incorrect order_id"):
        store.delete_an_order(incorrect_order_id)

def test_delete_non_existing_order(store: Store, generate_order_id, generate_pet_id, ship_date, create_order):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    create_order(order_id, pet_id, 1, ship_date, "placed", True)
    first_delete = store.delete_an_order(order_id)
    assert first_delete.ok

    second_delete = store.delete_an_order(order_id)
    assert second_delete.status == 404