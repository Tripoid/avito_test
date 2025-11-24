import pytest
import random

@pytest.fixture(scope="session")
def base_url():
    return "https://qa-internship.avito.com"

@pytest.fixture(scope="session")
def seller_id():
    return random.randint(111111, 999999)