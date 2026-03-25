"""
Pytest configuration and fixtures for the Mergington High School Activities API tests.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI application.
    
    Returns:
        TestClient: A test client for making requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def activities_fixture():
    """
    Provides a fresh copy of the activities database before each test.
    This ensures test isolation by resetting the global activities state.
    
    Yields:
        dict: A deep copy of the activities dictionary for testing.
    """
    # Create a deep copy to avoid test pollution
    original_activities = copy.deepcopy(activities)
    
    # Replace the app's activities with our copy
    app.dependency_overrides = {}
    
    yield activities
    
    # Restore the original activities after the test
    activities.clear()
    activities.update(original_activities)
