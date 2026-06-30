# Playwright API Petstore Testing

[![Petstore API - Test Suite](https://github.com/MateuszPason/Playwright_API_Petstore_Testing/actions/workflows/test_suite_run.yml/badge.svg)](https://github.com/MateuszPason/Playwright_API_Petstore_Testing/actions/workflows/test_suite_run.yml)

Automated API test suite for the [Swagger Petstore](https://petstore.swagger.io/) REST API, built with [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/).

## Overview

This project validates the Swagger Petstore API across the `/v2/pet`, `/v2/store`, and `/v2/user` endpoints, covering the full pet lifecycle, status filtering, image upload, store inventory and order management, and complete user management including login/logout session handling.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── pet_utils.py          # Pet API client wrapper (create, get, update, delete, upload)
│   ├── store_utils.py        # Store API client wrapper (inventory, orders)
│   ├── user_utils.py         # User API client wrapper (create, get, update, delete, login, logout)
│   └── models/
│       ├── __init__.py
│       ├── pet_models.py     # Pydantic models: PetPayload, PetResponse, Category, Tag
│       ├── store_models.py   # Pydantic models: OrderResponse
│       └── user_models.py    # Pydantic models: UserPayload, UserResponse
├── tests/
│   ├── conftest.py            # Shared pytest fixtures (session context, clients, helpers)
│   ├── assets/
│   │   └── images/            # Sample images used in upload tests
│   ├── pet/
│   │   ├── test_pet_create.py     # POST /v2/pet
│   │   ├── test_pet_delete.py     # DELETE /v2/pet/{petId}
│   │   ├── test_pet_get.py        # GET /v2/pet/{petId}
│   │   ├── test_pet_image_upload.py  # POST /v2/pet/{petId}/uploadImage
│   │   ├── test_pet_lifecycle.py  # End-to-end create → update → delete → verify
│   │   ├── test_pet_status.py     # GET /v2/pet/findByStatus
│   │   └── test_pet_update.py     # PUT /v2/pet
│   ├── store/
│   │   ├── test_store_delete_order.py    # DELETE /v2/store/order/{orderId}
│   │   ├── test_store_get.py             # GET /v2/store/inventory
│   │   ├── test_store_get_order.py       # GET /v2/store/order/{orderId}
│   │   └── test_store_place_an_order.py  # POST /v2/store/order
│   └── user/
│       ├── test_user_create.py    # POST /v2/user
│       ├── test_user_delete.py    # DELETE /v2/user/{username}
│       ├── test_user_get.py       # GET /v2/user/{username}
│       ├── test_user_login.py     # GET /v2/user/login
│       ├── test_user_logout.py    # GET /v2/user/logout
│       └── test_user_update.py    # PUT /v2/user/{username}
├── .gitignore
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- A virtual environment tool (e.g., `venv`)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Playwright_API_Petstore_Testing
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

## Running Tests

**Run all tests:**
```bash
pytest
```

**Run only pet tests:**
```bash
pytest tests/pet
```

**Run only store tests:**
```bash
pytest tests/store
```

**Run only user tests:**
```bash
pytest tests/user
```

**Run smoke tests only:**
```bash
pytest -m smoke
```

**Run regression tests only:**
```bash
pytest -m regression
```

**Run a specific test file:**
```bash
pytest tests/pet/test_pet_create.py
```

**Run a specific test by name:**
```bash
pytest -k "test_get_existing_pet"
```

**Run with verbose output:**
```bash
pytest -v
```

**Run with a live log stream:**
```bash
pytest -v --log-cli-level=INFO
```

## Test Coverage

| File | Endpoint | Scenarios Covered |
|------|----------|-------------------|
| `test_pet_create.py` | `POST /v2/pet` | Successful creation (200), wrong HTTP method (405) |
| `test_pet_get.py` | `GET /v2/pet/{petId}` | Existing pet (200), non-existing pet (404) |
| `test_pet_update.py` | `PUT /v2/pet` | Successful update, invalid field data type (500) |
| `test_pet_delete.py` | `DELETE /v2/pet/{petId}` | Existing pet (200), non-existing pet (404) |
| `test_pet_status.py` | `GET /v2/pet/findByStatus` | Valid statuses (`available`, `pending`, `sold`), invalid/missing status |
| `test_pet_image_upload.py` | `POST /v2/pet/{petId}/uploadImage` | JPG and PNG uploads (200), no file provided (415) |
| `test_pet_lifecycle.py` | Multiple | Full end-to-end: create → update → delete → verify deletion |
| `test_store_get.py` | `GET /v2/store/inventory` | Inventory contains created statuses, unknown statuses are absent, repeated inventory calls are stable |
| `test_store_get_order.py` | `GET /v2/store/order/{orderId}` | Existing order (200), non-existing order (404), invalid order ID (ValueError) |
| `test_store_place_an_order.py` | `POST /v2/store/order` | Successful placement across all status/complete combos, invalid order ID / pet ID / quantity / ship date / status / complete (ValueError) |
| `test_store_delete_order.py` | `DELETE /v2/store/order/{orderId}` | Successful delete (200), delete non-existing order (404), invalid order ID (ValueError) |
| `test_user_create.py` | `POST /v2/user` | Successful creation (200), response schema validation, persistence check, no body provided (415) |
| `test_user_get.py` | `GET /v2/user/{username}` | Existing user (200), non-existing user (404), invalid username (ValueError) |
| `test_user_update.py` | `PUT /v2/user/{username}` | Successful update with field verification, update non-existing user (xfail — broken endpoint returns 200) |
| `test_user_delete.py` | `DELETE /v2/user/{username}` | Successful delete (200), response body check, delete non-existing user (404), invalid username (ValueError) |
| `test_user_login.py` | `GET /v2/user/login` | Successful login (200), required response fields, `x-rate-limit` header, `x-expires-after` header, unique session token per login |
| `test_user_logout.py` | `GET /v2/user/logout` | Successful logout (200) |

## Key Components

### `Pet` Client (`src/pet_utils.py`)

A thin wrapper around Playwright's `APIRequestContext` that exposes one method per HTTP operation. `get_pet` and `delete_pet` validate that `pet_id` is a positive integer and raise `ValueError` otherwise.

| Method | HTTP Verb | Description |
|--------|-----------|-------------|
| `create_pet(**kwargs)` | POST | Add a new pet |
| `get_pet(pet_id, **kwargs)` | GET | Retrieve a pet by ID |
| `update_pet(**kwargs)` | PUT | Update an existing pet |
| `delete_pet(pet_id, **kwargs)` | DELETE | Remove a pet |
| `get_pet_by_status(status=None, **kwargs)` | GET | Find pets by status |
| `upload_image(endpoint, file_path, additional_metadata, **kwargs)` | POST | Upload a pet image |

### `User` Client (`src/user_utils.py`)

`delete_user`, `get_user`, `update_user`, and `login_user` validate their inputs and raise `ValueError` on invalid values (empty or non-string username/password).

| Method | HTTP Verb | Description |
|--------|-----------|-------------|
| `create_user(**kwargs)` | POST | Create a new user |
| `get_user(username, **kwargs)` | GET | Retrieve a user by username |
| `update_user(username, **kwargs)` | PUT | Update an existing user by username |
| `delete_user(username, **kwargs)` | DELETE | Remove a user by username |
| `login_user(username, password, **kwargs)` | GET | Log in and receive a session token |
| `logout_user(**kwargs)` | GET | Log out the current session |

### `Store` Client (`src/store_utils.py`)

`get_order_by_id`, `place_an_order`, and `delete_an_order` validate their inputs and raise `ValueError` on invalid values.

| Method | HTTP Verb | Description |
|--------|-----------|-------------|
| `get_pet_inventories_in_store(**kwargs)` | GET | Retrieve store inventory counts |
| `get_order_by_id(order_id, **kwargs)` | GET | Retrieve a store order by ID |
| `place_an_order(order_id, pet_id, quantity, ship_date, status, complete, **kwargs)` | POST | Place a new store order with input validation |
| `delete_an_order(order_id)` | DELETE | Delete a store order by ID |

### Models (`src/models/`)

All models are [Pydantic](https://docs.pydantic.dev/) `BaseModel` subclasses used for payload construction and response validation.

**`pet_models.py`**

| Model | Description |
|-------|-------------|
| `Category` | Pet category with `id` and `name` |
| `Tag` | Pet tag with `id` and `name` |
| `PetPayload` | Full pet request schema: `id`, `category`, `name`, `photoUrls`, `tags`, `status` |
| `PetResponse` | Expected pet response schema mirroring the Petstore API response shape |

**`store_models.py`**

| Model | Description |
|-------|-------------|
| `OrderResponse` | Expected order response schema: `id`, `petId`, `quantity`, `shipDate`, `status`, `complete` |

**`user_models.py`**

| Model | Description |
|-------|-------------|
| `UserPayload` | Full user request schema: `id`, `username`, `firstName`, `lastName`, `email`, `password`, `phone`, `userStatus` |
| `UserResponse` | Expected user response schema mirroring the Petstore API response shape |

### Fixtures (`tests/conftest.py`)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `api_request_context` | session | Shared Playwright API context using `BASE_URL` from `.env` |
| `pet` | function | `Pet` client instance |
| `store` | function | `Store` client instance |
| `user` | function | `User` client instance |
| `new_pet` | function | Default `PetPayload` instance for create scenarios |
| `updated_pet` | function | `PetPayload` instance with modified fields for update scenarios |
| `new_user` | function | Default `UserPayload` instance with a randomly generated username for create scenarios |
| `updated_user` | function | `UserPayload` instance with modified fields for user update scenarios |
| `generate_id` | function | Generates a random integer ID via UUID (used for both pet and user IDs) |
| `init_pet` | function | Helper to create a pet from a `PetPayload` |
| `init_user` | function | Helper to create a user from a `UserPayload` |
| `pet_cleanup` | function | Helper to delete a pet by ID |
| `user_cleanup` | function | Helper that collects usernames and deletes them all after the test |
| `generate_random_string` | function | Generates random strings for pet status and inventory tests |
| `generate_order_id` | function | Generates a random integer order ID (11–1000) |
| `ship_date` | function | Returns current UTC timestamp in ISO-8601 format for use in order payloads |
| `create_order` | function | Helper to place a store order via `Store.place_an_order` |
| `order_cleanup` | function | Helper to delete a store order by ID |

## Dependencies

| Package | Purpose |
|---------|---------|
| `playwright` | API request context and HTTP client |
| `pytest` | Test runner and fixture engine |
| `pytest-playwright` | Playwright integration for pytest |
| `pytest-base-url` | `--base-url` CLI flag support |
| `pytest-html` | HTML report generation |
| `pydantic` | Payload and response model validation |
| `python-dotenv` | `.env` file loading |
| `requests` | Supplementary HTTP utilities |

See [requirements.txt](requirements.txt) for pinned versions.

## Test Markers

Tests are tagged with pytest markers defined in `pytest.ini`:

| Marker | Purpose |
|--------|---------|
| `smoke` | Sanity checks — fast, high-confidence tests covering the happy path of each endpoint |
| `regression` | Full regression suite — covers edge cases, error paths, schema validation, and header assertions |

## Notes

- Pet and user IDs are randomly generated per test run using UUID to minimise collisions against a shared public API.
- Tests that create pets or users include cleanup calls to avoid polluting the Petstore sandbox.
- The `user_cleanup` fixture collects all usernames registered during a test and deletes them in bulk after the test completes.
- Store inventory tests create temporary pets with random statuses so they can assert inventory counts deterministically.
- The image upload test does not assert that the uploaded image is retrievable from the pet object, as the public Petstore API does not return image data in `GET /v2/pet/{petId}` responses at this time.
- `test_update_non_existing_user` is marked `xfail` because the `PUT /v2/user/{username}` endpoint returns `200` for non-existing usernames instead of the expected `404`.
