"""
Tests for activity signup and participant management endpoints
using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi import HTTPException


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful_for_new_student(self, client, sample_email, existing_activity_name):
        """
        Test successful signup of a new student to an existing activity.
        
        AAA Pattern:
        - Arrange: Prepare valid activity and email
        - Act: Send POST request to signup endpoint
        - Assert: Student is added and success message returned
        """
        # Arrange
        email = "new_student_test@mergington.edu"
        signup_url = f"/activities/{existing_activity_name}/signup"
        params = {"email": email}
        
        # Act
        response = client.post(signup_url, params=params)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert existing_activity_name in data["message"]

    def test_signup_returns_confirmation_message(self, client):
        """
        Test that signup returns a proper confirmation message.
        
        AAA Pattern:
        - Arrange: Valid signup data prepared
        - Act: Send POST request to signup endpoint
        - Assert: Response message contains both email and activity name
        """
        # Arrange
        email = "participant_test@mergington.edu"
        activity = "Tennis Club"
        url = f"/activities/{activity}/signup"
        
        # Act
        response = client.post(url, params={"email": email})
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert f"Signed up {email}" in message
        assert activity in message

    def test_signup_fails_for_nonexistent_activity(self, client, non_existent_activity_name, sample_email):
        """
        Test that signup fails with 404 for non-existent activity.
        
        AAA Pattern:
        - Arrange: Prepare signup with non-existent activity
        - Act: Send POST request to signup endpoint
        - Assert: Response is 404 with error message
        """
        # Arrange
        url = f"/activities/{non_existent_activity_name}/signup"
        params = {"email": sample_email}
        expected_detail = "Activity not found"
        
        # Act
        response = client.post(url, params=params)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == expected_detail

    def test_signup_fails_when_student_already_signed_up(self, client, existing_activity_name):
        """
        Test that signup fails when student is already signed up.
        
        AAA Pattern:
        - Arrange: Use existing participant who is already signed up
        - Act: Send POST request to signup endpoint with their email
        - Assert: Response is 400 with duplicate signup error
        """
        # Arrange
        email = "emma@mergington.edu"  # Already in Programming Class
        url = f"/activities/{existing_activity_name}/signup"
        params = {"email": email}
        
        # Act
        response = client.post(url, params=params)
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        assert response.json()["detail"] == "Student is already signed up for this activity"

    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Test that multiple different students can sign up to the same activity.
        
        AAA Pattern:
        - Arrange: Prepare two different student emails
        - Act: Sign up both students to the same activity
        - Assert: Both signups succeed with 200 status
        """
        # Arrange
        activity = "Art Club"
        email_one = "first_new_student@mergington.edu"
        email_two = "second_new_student@mergington.edu"
        url = f"/activities/{activity}/signup"
        
        # Act - Sign up first student
        response_one = client.post(url, params={"email": email_one})
        
        # Assert - First signup succeeds
        assert response_one.status_code == 200
        
        # Act - Sign up second student
        response_two = client.post(url, params={"email": email_two})
        
        # Assert - Second signup also succeeds
        assert response_two.status_code == 200

    def test_signup_returns_proper_http_status(self, client):
        """
        Test that signup returns appropriate HTTP status codes.
        
        AAA Pattern:
        - Arrange: Prepare different signup scenarios
        - Act: Send requests with valid data
        - Assert: Get HTTP 200 for successful signup
        """
        # Arrange
        email = "status_test@mergington.edu"
        activity = "Drama Club"
        url = f"/activities/{activity}/signup"
        
        # Act
        response = client.post(url, params={"email": email})
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_successfully(self, client):
        """
        Test successful removal of a participant from an activity.
        
        AAA Pattern:
        - Arrange: First sign up a student, then prepare removal
        - Act: Send DELETE request to remove endpoint
        - Assert: Participant is removed and success message returned
        """
        # Arrange
        email = "removal_test@mergington.edu"
        activity = "Science Club"
        signup_url = f"/activities/{activity}/signup"
        remove_url = f"/activities/{activity}/participants/{email}"
        
        # Sign up the student first
        client.post(signup_url, params={"email": email})
        
        # Act
        response = client.delete(remove_url)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_remove_participant_returns_confirmation_message(self, client):
        """
        Test that removal returns a proper confirmation message.
        
        AAA Pattern:
        - Arrange: Sign up a student and prepare removal
        - Act: Send DELETE request to remove participant
        - Assert: Response message confirms removal
        """
        # Arrange
        email = "removal_confirmation_test@mergington.edu"
        activity = "Debate Team"
        signup_url = f"/activities/{activity}/signup"
        remove_url = f"/activities/{activity}/participants/{email}"
        
        # Sign up
        client.post(signup_url, params={"email": email})
        
        # Act
        response = client.delete(remove_url)
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert f"Removed {email} from {activity}" in message

    def test_remove_participant_from_nonexistent_activity(self, client, sample_email, non_existent_activity_name):
        """
        Test that removal fails with 404 for non-existent activity.
        
        AAA Pattern:
        - Arrange: Prepare removal from non-existent activity
        - Act: Send DELETE request
        - Assert: Response is 404 with error message
        """
        # Arrange
        url = f"/activities/{non_existent_activity_name}/participants/{sample_email}"
        expected_detail = "Activity not found"
        
        # Act
        response = client.delete(url)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == expected_detail

    def test_remove_participant_not_in_activity(self, client, existing_activity_name):
        """
        Test that removal fails with 404 when participant is not in the activity.
        
        AAA Pattern:
        - Arrange: Prepare removal of non-participant
        - Act: Send DELETE request with email not in activity
        - Assert: Response is 404 with participant not found error
        """
        # Arrange
        email = "not_participant@mergington.edu"
        url = f"/activities/{existing_activity_name}/participants/{email}"
        expected_detail = "Participant not found in this activity"
        
        # Act
        response = client.delete(url)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == expected_detail

    def test_remove_existing_participant_from_activity(self, client):
        """
        Test removal of a participant who is already in the activity list.
        
        AAA Pattern:
        - Arrange: Use existing participant from initial data
        - Act: Send DELETE request to remove them
        - Assert: Removal succeeds with 200 status
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        url = f"/activities/{activity}/participants/{email}"
        
        # Act
        response = client.delete(url)
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_cannot_remove_same_participant_twice(self, client):
        """
        Test that removing the same participant twice fails on second attempt.
        
        AAA Pattern:
        - Arrange: Sign up a student and remove them once
        - Act: Attempt to remove them again
        - Assert: Second removal fails with 404
        """
        # Arrange
        email = "double_removal_test@mergington.edu"
        activity = "Tennis Club"
        signup_url = f"/activities/{activity}/signup"
        remove_url = f"/activities/{activity}/participants/{email}"
        
        # Sign up the student
        client.post(signup_url, params={"email": email})
        
        # Remove once (should succeed)
        response_one = client.delete(remove_url)
        assert response_one.status_code == 200
        
        # Act - Try to remove again
        response_two = client.delete(remove_url)
        
        # Assert - Second removal fails
        assert response_two.status_code == 404
        assert response_two.json()["detail"] == "Participant not found in this activity"

    def test_remove_participant_returns_proper_http_status(self, client):
        """
        Test that removal endpoint returns appropriate HTTP status codes.
        
        AAA Pattern:
        - Arrange: Prepare removal scenario
        - Act: Send DELETE request
        - Assert: Verify correct status code and headers
        """
        # Arrange
        email = "status_removal_test@mergington.edu"
        activity = "Art Club"
        signup_url = f"/activities/{activity}/signup"
        remove_url = f"/activities/{activity}/participants/{email}"
        
        # Set up by signing up
        client.post(signup_url, params={"email": email})
        
        # Act
        response = client.delete(remove_url)
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"


class TestActivityDataIntegrity:
    """Test suite for ensuring data integrity across operations."""

    def test_signup_actually_adds_participant_to_activity(self, client):
        """
        Test that signup actually adds the participant to the activity list.
        
        AAA Pattern:
        - Arrange: Prepare signup and get initial state
        - Act: Sign up a student and retrieve activities
        - Assert: Participant is in the activity list
        """
        # Arrange
        email = "integrity_test@mergington.edu"
        activity = "Science Club"
        
        # Act - Sign up
        signup_url = f"/activities/{activity}/signup"
        client.post(signup_url, params={"email": email})
        
        # Act - Retrieve activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert email in data[activity]["participants"]

    def test_removal_actually_removes_participant_from_activity(self, client):
        """
        Test that removal actually removes the participant from the activity list.
        
        AAA Pattern:
        - Arrange: Sign up a participant
        - Act: Remove them and retrieve activities
        - Assert: Participant is no longer in the activity list
        """
        # Arrange
        email = "removal_integrity@mergington.edu"
        activity = "Debate Team"
        
        # Sign up first
        signup_url = f"/activities/{activity}/signup"
        client.post(signup_url, params={"email": email})
        
        # Act - Remove
        remove_url = f"/activities/{activity}/participants/{email}"
        client.delete(remove_url)
        
        # Act - Retrieve activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert email not in data[activity]["participants"]
