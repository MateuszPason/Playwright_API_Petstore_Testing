from src.store_utils import Store
import pytest

@pytest.mark.regression
@pytest.mark.parametrize(
    "status, complete",
    [
        ("placed", True),
        ("placed", False),
        ("approved", True),
        ("approved", False),
        ("delivered", True),
        ("delivered", False),
    ],
)
def test_successful_order_placement(
    store: Store, generate_order_id, generate_pet_id, ship_date, status, complete, order_cleanup
):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    order_response = store.place_an_order(order_id, pet_id, 1, ship_date, status, complete)
    assert order_response.ok

    created_order_body = store.get_order_by_id(order_id).json()
    assert created_order_body["id"] == order_id
    assert created_order_body["petId"] == pet_id
    assert created_order_body["quantity"] == 1
    assert created_order_body["shipDate"] == ship_date
    assert created_order_body["status"] == status
    assert created_order_body["complete"] is complete

    order_cleanup(order_id)

@pytest.mark.parametrize("incorrect_order_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_order_id(store: Store, incorrect_order_id, generate_pet_id, ship_date):
    pet_id = generate_pet_id()

    with pytest.raises(ValueError, match="Incorrect order_id"):
        store.place_an_order(incorrect_order_id, pet_id, 1, ship_date, "placed", False)

@pytest.mark.parametrize("incorrect_pet_id", [0, -1, True, False, "123", None, 1.5])
def test_incorrect_pet_id(store: Store, generate_order_id, ship_date, incorrect_pet_id):
    order_id = generate_order_id()

    with pytest.raises(ValueError, match="Incorrect pet_id"):
        store.place_an_order(order_id, incorrect_pet_id, 1, ship_date, "placed", False)

@pytest.mark.parametrize("incorrect_quantity", [0, -1, True, False, "1", None, 1.5])
def test_incorrect_quantity(
    store: Store, generate_order_id, generate_pet_id, ship_date, incorrect_quantity
):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    with pytest.raises(ValueError, match="Incorrect quantity"):
        store.place_an_order(
            order_id, pet_id, incorrect_quantity, ship_date, "placed", False
        )

@pytest.mark.parametrize("incorrect_ship_date", [None, 123, 1.5, True, False, [], {}])
def test_ship_date(
    store: Store, generate_order_id, generate_pet_id, incorrect_ship_date
):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    with pytest.raises(ValueError, match="Incorrect ship_date"):
        store.place_an_order(order_id, pet_id, 1, incorrect_ship_date, "placed", False)

@pytest.mark.parametrize("incorrect_status", ["new", "in_progress"])
def test_incorrect_status(
    store: Store, generate_order_id, generate_pet_id, ship_date, incorrect_status
):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    with pytest.raises(ValueError, match="Incorrect status"):
        store.place_an_order(order_id, pet_id, 1, ship_date, incorrect_status, False)

@pytest.mark.parametrize(
    "incorrect_complete_value", ["1", "0", "True", "False", "", " "]
)
def test_incorrect_complete_value(
    store: Store, generate_order_id, generate_pet_id, ship_date, incorrect_complete_value
):
    order_id = generate_order_id()
    pet_id = generate_pet_id()

    with pytest.raises(ValueError, match="Incorrect complete value"):
        store.place_an_order(
            order_id, pet_id, 1, ship_date, "placed", incorrect_complete_value
        )
