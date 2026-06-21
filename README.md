# Playwright API Petstore Testing

Automated API test suite for the [Swagger Petstore](https://petstore.swagger.io/) REST API, built with [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/).

## Overview

This project validates the `/v2/pet` endpoints of the Petstore API, covering the full CRUD lifecycle as well as status filtering and image upload functionality.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── pet_utils.py          # Pet API client wrapper (create, get, update, delete, upload)
├── tests/
│   ├── conftest.py            # Shared pytest fixtures (session context, pet client, helpers)
│   ├── assets/
│   │   └── images/            # Sample images used in upload tests
│   │       ├── solid_blue.jpg
│   │       └── solid_blue.png
│   ├── payloads/
│   │   ├── __init__.py
│   │   └── pet_payloads.py    # Reusable PetPayload dataclass and preset payloads
│   └── pet/
│       ├── test_pet_create.py     # POST /v2/pet
│       ├── test_pet_delete.py     # DELETE /v2/pet/{petId}
│       ├── test_pet_get.py        # GET /v2/pet/{petId}
│       ├── test_pet_image_upload.py  # POST /v2/pet/{petId}/uploadImage
│       ├── test_pet_lifecycle.py  # End-to-end create → update → delete → verify
│       ├── test_pet_status.py     # GET /v2/pet/findByStatus
│       └── test_pet_update.py     # PUT /v2/pet
├── .env                       # Environment variables (not committed)
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

5. **Configure environment variables:**

   Create a `.env` file in the project root:
   ```
   BASE_URL=https://petstore.swagger.io
   ```

## Running Tests

**Run all tests:**
```bash
pytest
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

## Key Components

### `Pet` Client (`src/pet_utils.py`)

A thin wrapper around Playwright's `APIRequestContext` that exposes one method per HTTP operation:

| Method | HTTP Verb | Description |
|--------|-----------|-------------|
| `create_pet(endpoint, **kwargs)` | POST | Add a new pet |
| `get_pet(endpoint, **kwargs)` | GET | Retrieve a pet by ID |
| `update_pet(endpoint, **kwargs)` | PUT | Update an existing pet |
| `delete_pet(endpoint, **kwargs)` | DELETE | Remove a pet |
| `get_pet_by_status(endpoint, status, **kwargs)` | GET | Find pets by status |
| `upload_image(endpoint, file_path, additional_metadata, **kwargs)` | POST | Upload a pet image |

### Fixtures (`tests/conftest.py`)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `api_request_context` | session | Shared Playwright API context using `BASE_URL` from `.env` |
| `pet` | function | `Pet` client instance |
| `generate_pet_id` | function | Generates a random integer pet ID via UUID |
| `init_pet` | function | Helper to create a pet from a `PetPayload` |
| `pet_cleanup` | function | Helper to delete a pet by ID |

### Payloads (`tests/payloads/pet_payloads.py`)

`PetPayload` is a `dataclass` defining the full pet schema. Two preset instances are provided:

- `CREATE_PET` — baseline payload for creating a test pet
- `UPDATE_PET` — payload with modified fields for update scenarios

## Dependencies

| Package | Purpose |
|---------|---------|
| `playwright` | API request context and HTTP client |
| `pytest` | Test runner and fixture engine |
| `pytest-playwright` | Playwright integration for pytest |
| `pytest-base-url` | `--base-url` CLI flag support |
| `python-dotenv` | `.env` file loading |
| `requests` | Supplementary HTTP utilities |

See [requirements.txt](requirements.txt) for pinned versions.

## Notes

- Pet IDs are randomly generated per test run using UUID to minimise collisions against a shared public API.
- Tests that create pets include cleanup calls to avoid polluting the Petstore sandbox.
- The image upload test does not assert that the uploaded image is retrievable from the pet object, as the public Petstore API does not return image data in `GET /v2/pet/{petId}` responses at this time.
