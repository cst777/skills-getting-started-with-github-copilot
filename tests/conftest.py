"""
Pytest configuration and fixtures for the Mergington High School API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provide a TestClient instance for testing FastAPI endpoints.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """
    Provide a sample student email for testing.
    """
    return "test_student@mergington.edu"


@pytest.fixture
def existing_participant_email():
    """
    Provide an email of a participant already in an activity.
    """
    return "emma@mergington.edu"


@pytest.fixture
def existing_activity_name():
    """
    Provide the name of an activity that exists in the system.
    """
    return "Programming Class"


@pytest.fixture
def non_existent_activity_name():
    """
    Provide the name of an activity that doesn't exist.
    """
    return "Non Existent Activity"
