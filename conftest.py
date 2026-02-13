import os
import pytest

@pytest.fixture(scope="session")
def django_env():
    os.environ.setdefault("LIFEOS_ENV", "development")
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
