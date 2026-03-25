"""
Tests for POST /activities/{activity_name}/signup endpoint.

Tests verify that students can successfully sign up for activities,
and that appropriate errors are returned for invalid requests.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_happy_path(self, client, activities_fixture):
        """
        Test that a student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Select an activity and a new student email
        - Act: Make POST request to signup endpoint
        - Assert: Verify response success and student is added to participants
        """
        # Arrange: Set up test data
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act: Make the signup request
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: Verify response and state
        assert response.status_code == 200
        assert email in activities_fixture[activity_name]["participants"]
        result = response.json()
        assert "message" in result
        assert email in result["message"]
    
    def test_signup_activity_not_found(self, client, activities_fixture):
        """
        Test that signup fails with 404 when activity doesn't exist.
        
        AAA Pattern:
        - Arrange: Use a non-existent activity name
        - Act: Make POST request to signup endpoint
        - Assert: Verify 404 response
        """
        # Arrange: Set up test data with non-existent activity
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act: Make the signup request
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]
    
    def test_signup_duplicate_student(self, client, activities_fixture):
        """
        Test that signup fails with 400 when student already signed up.
        
        AAA Pattern:
        - Arrange: Use an activity and a student already in participants
        - Act: Make POST request to signup endpoint
        - Assert: Verify 400 error response
        """
        # Arrange: Use existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act: Try to sign up again
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: Verify error response
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"]
    
    def test_signup_adds_to_participants_list(self, client, activities_fixture):
        """
        Test that signup correctly updates the participants list.
        
        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Make POST request to signup
        - Assert: Verify participant count increased by 1
        """
        # Arrange: Record initial state
        activity_name = "Art Studio"
        email = "newartist@mergington.edu"
        initial_count = len(activities_fixture[activity_name]["participants"])
        
        # Act: Sign up for the activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: Verify participant was added
        assert response.status_code == 200
        updated_count = len(activities_fixture[activity_name]["participants"])
        assert updated_count == initial_count + 1
        assert email in activities_fixture[activity_name]["participants"]
    
    def test_signup_with_numeric_email(self, client, activities_fixture):
        """
        Test that signup works with emails containing numbers.
        
        AAA Pattern:
        - Arrange: Create an email with numbers
        - Act: Make POST request to signup
        - Assert: Verify success and participant is added
        """
        # Arrange: Use email with numbers
        activity_name = "Science Lab"
        email = "student123@mergington.edu"
        
        # Act: Make the signup request
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: Verify success
        assert response.status_code == 200
        assert email in activities_fixture[activity_name]["participants"]
