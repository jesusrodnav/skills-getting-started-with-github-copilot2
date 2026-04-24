import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_200(self, test_client, reset_activities):
        """
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: Verify status code is 200
        """
        # Arrange
        # (test_client and reset_activities fixtures already arranged)
        
        # Act
        response = test_client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, test_client, reset_activities):
        """
        Arrange: Set up test client with reset activities (9 activities total)
        Act: Make GET request to /activities
        Assert: Verify all 9 activities are returned
        """
        # Arrange
        expected_count = 9
        
        # Act
        response = test_client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == expected_count
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_activities_correct_structure(self, test_client, reset_activities):
        """
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = test_client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_get_activities_participant_counts_accurate(self, test_client, reset_activities):
        """
        Arrange: Set up test client with known participant counts
        Act: Make GET request to /activities
        Assert: Verify participant counts match expected values
        """
        # Arrange
        expected_participants = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Basketball Team": 0,
            "Soccer Club": 0,
        }
        
        # Act
        response = test_client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, expected_count in expected_participants.items():
            actual_count = len(data[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} should have {expected_count} participants, got {actual_count}"
