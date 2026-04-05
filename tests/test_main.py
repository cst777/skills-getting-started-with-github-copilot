"""
Tests for main API endpoints using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRootEndpoint:
    """Test suite for the root endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that the root endpoint redirects to the static index page.
        
        AAA Pattern:
        - Arrange: TestClient is ready
        - Act: Send GET request to /
        - Assert: Response is a redirect to /static/index.html
        """
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestActivitiesListEndpoint:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: TestClient is ready
        - Act: Send GET request to /activities
        - Assert: Response contains all activities with correct structure
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Club",
            "Drama Club",
            "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]

    def test_get_activities_has_correct_activity_details(self, client):
        """
        Test that GET /activities returns activities with correct details.
        
        AAA Pattern:
        - Arrange: Expected activity structure is defined
        - Act: Send GET request to /activities
        - Assert: Activity data matches expected structure
        """
        # Arrange
        activity_name = "Programming Class"
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert activity_name in data
        assert set(data[activity_name].keys()) == expected_keys
        assert isinstance(data[activity_name]["participants"], list)
        assert data[activity_name]["max_participants"] > 0

    def test_get_activities_has_participants_list(self, client):
        """
        Test that activities include participant information.
        
        AAA Pattern:
        - Arrange: ActivityList endpoint should return participants
        - Act: Send GET request to /activities
        - Assert: Participants are present and are email addresses
        """
        # Arrange
        # Activity "Chess Club" has known participants
        expected_participant = "daniel@mergington.edu"  # Use participant that won't be removed by other tests
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert "Chess Club" in data
        assert expected_participant in data["Chess Club"]["participants"]
