import pytest
from playwright.sync_api import Playwright, APIRequestContext
from src.pet_utils import Pet
from src.store_utils import Store
from src.user_utils import User
import uuid
import secrets
import string
from datetime import datetime, timezone
from src.models.pet_models import PetPayload, Category, Tag
from src.models.user_models import UserPayload

@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright, base_url: str):
    api_context = playwright.request.new_context(
        base_url= base_url
    )
    yield api_context
    api_context.dispose()

@pytest.fixture
def pet(api_request_context: APIRequestContext):
    return Pet(api_request_context)

@pytest.fixture
def store(api_request_context: APIRequestContext):
    return Store(api_request_context)

@pytest.fixture
def user(api_request_context: APIRequestContext):
    return User(api_request_context)

@pytest.fixture
def pet_cleanup(pet: Pet):
    pet_ids = []
    def _cleanup(pet_id: int):
        pet_ids.append(pet_id)
    yield _cleanup

    for pet_id in pet_ids:
        pet.delete_pet(pet_id)

@pytest.fixture
def user_cleanup(user: User):
    usernames = []
    def _cleanup(username: str):
        usernames.append(username)
    yield _cleanup

    for username in usernames:
        user.delete_user(username)

@pytest.fixture
def new_pet():
    return PetPayload(
        id=None,
        category=Category(id=101, name="TestingPet"),
        name="TestingPet101",
        photoUrls=[""],
        tags=[Tag(id=101, name="101Pet")],
        status="available",
    )

@pytest.fixture
def updated_pet():
    return PetPayload(
        id=None,
        category=Category(id=102, name="TestingPet - Updated"),
        name="TestingPet101 - Updated",
        photoUrls=["https://testphoto.jpg"],
        tags=[Tag(id=102, name="101Pet - Updated")],
        status="available - Updated",
    )

@pytest.fixture
def new_user():
    return UserPayload(
        id=None,
        username=uuid.uuid4().hex[:10],
        firstName="TestingFN",
        lastName="TestingLN",
        email="test@test.com",
        password="test1234",
        phone="123123123",
        userStatus=1
    )

@pytest.fixture
def updated_user():
    return UserPayload(
        id=None,
        username=uuid.uuid4().hex[:10],
        firstName="TestingFN - Updated",
        lastName="TestingLN - Updated",
        email="test+updated@test.com",
        password="test1234Updated",
        phone="321321321",
        userStatus=2
    )

@pytest.fixture
def init_pet(pet: Pet):
    def _init(pet_data: PetPayload):
        return pet.create_pet(data=pet_data.model_dump())
    return _init

@pytest.fixture
def init_user(user: User):
    def _init(user_data: UserPayload):
        return user.create_user(data=user_data.model_dump())
    return _init

@pytest.fixture
def generate_id():
    def _generate():
        return int(uuid.uuid4().int % 100000)
    return _generate

@pytest.fixture
def generate_random_string(length=8):
    def _generate():
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
    return _generate

@pytest.fixture
def generate_order_id():
    def _generate():
        return int(uuid.uuid4().int % 990) + 11
    return _generate

@pytest.fixture
def ship_date():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "+0000")

@pytest.fixture
def create_order(store: Store):
    def _init(order_id, pet_id, quantity, ship_date, status, complete):
        return store.place_an_order(order_id, pet_id, quantity, ship_date, status, complete)
    return _init

@pytest.fixture
def order_cleanup(store: Store):
    order_ids = []
    def _cleanup(order_id):
        order_ids.append(order_id)
    yield _cleanup

    for order_id in order_ids:
        store.delete_an_order(order_id)