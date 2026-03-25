"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.

Tests verify that students can successfully unregister from activities,
and that appropriate errors are returned for invalid requests.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_happy_path(self, client, activities_fixture):
        """
        Test that a student can successfully unregister from an activity.
        
        AAA Pattern:
        - Arrange: Select an activity and an enrolled student
        - Act: Make DELETE request to unregister endpoint
        - Assert: Verify response success and student is removed from participants
        """
        # Arrange: Use an existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled
        
        # Act: Make the unregister request
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: Verify response and state
        assert response.status_code == 200
        assert email not in activities_fixture[activity_name]["participants"]
        result = response.json()
        assert "message" in result
        assert "Unregistered" in result["message"]
    
    def test_unregister_activity_not_found(self, client, activities_fixture):
        """
        Test that unregister fails with 404 when activity doesn't exist.
        
        AAA Pattern:
        - Arrange: Use a non-existent activity name
        - Act: Make DELETE request to unregister endpoint
        - Assert: Verify 404 response
        """
        # Arrange: Set up test data with non-existent activity
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act: Make the unregister request
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]
    
    def test_unregister_student_not_registered(self, client, activities_fixture):
        """
        Test that unregister fails with 400 when student is not enrolled.
        
        AAA Pattern:
        - Arrange: Use a student who is not in the participants list
        - Act: Make DELETE request to unregister endpoint
        - Assert: Verify 400 error response
        """
        # Arrange: Use a student not in Chess Club
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Verify student is not registered (sanity check)
        assert email not in activities_fixture[activity_name]["participants"]
        
        # Act: Try to unregister
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: Verify error response
        assert response.status_code == 400
        result = response.json()
        assert "not registered" in result["detail"]
    
    def test_unregister_removes_from_participants_list(self, client, activities_fixture):
        """
        Test that unregister correctly updates the participants list.
        
        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Make DELETE request to unregister
        - Assert: Verify participant count decreased by 1
        """
        # Arrange: Record initial state
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already enrolled
        initial_count = len(activities_fixture[activity_name]["participants"])
        
        # Act: Unregister from the activity
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: Verify participant was removed
        assert response.status_code == 200
        updated_count = len(activities_fixture[activity_name]["participants"])
        assert updated_count == initial_count - 1
        assert email not in activities_fixture[activity_name]["participants"]
    
    def test_unregister_multiple_participants(self, client, activities_fixture):
        """
        Test unregistering one participant doesn't affect others.
        
        AAA Pattern:
        - Arrange: Select an activity with multiple participants
        - Act: Unregister one participant
        - Assert: Verify other participants remain enrolled
        """
        # Arrange: Select an activity with multiple participants
        activity_name = "Music Band"  # Has noah and grace
        email_to_remove = "noah@mergington.edu"
        email_to_keep = "grace@mergington.edu"
        
        # Act: Unregister one participant
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email_to_remove}"
        )
        
        # Assert: Verify correct participant removed, others unaffected
        assert response.status_code == 200
        assert email_to_remove not in activities_fixture[activity_name]["participants"]
        assert email_to_keep in activities_fixture[activity_name]["participants"]
