"""
Tests for GET /activities endpoint.

Tests verify that the API correctly returns all available activities
with their details and participant information.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, activities_fixture):
        """
        Test that GET /activities returns all activities.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Response contains all activity names
        """
        # Arrange: No setup needed, client fixture handles it
        
        # Act: Make the GET request
        response = client.get("/activities")
        
        # Assert: Verify response status and content
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) > 0
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_returns_correct_activity_structure(self, client, activities_fixture):
        """
        Test that each activity has the expected structure.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Verify activity structure
        """
        # Arrange: No setup needed
        
        # Act: Make the GET request
        response = client.get("/activities")
        
        # Assert: Verify each activity has required fields
        activities = response.json()
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_includes_participant_count(self, client, activities_fixture):
        """
        Test that activities show correct participant counts.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Verify participant counts match
        """
        # Arrange: No setup needed
        
        # Act: Make the GET request
        response = client.get("/activities")
        
        # Assert: Verify participant lists are populated
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) > 0
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
