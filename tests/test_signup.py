import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful_200(self, test_client, reset_activities):
        """
        Arrange: Set up test client and valid activity/email
        Act: Submit signup request
        Assert: Verify status code is 200 and success message returned
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "alice@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
    
    def test_signup_adds_participant_to_activity(self, test_client, reset_activities):
        """
        Arrange: Set up test client and verify participant not in activity
        Act: Submit signup request
        Assert: Verify participant is now in activity's participants list
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "bob@mergington.edu"
        
        # Before signup, participant should not be in list
        response_before = test_client.get("/activities")
        participants_before = response_before.json()[activity_name]["participants"]
        assert email not in participants_before
        
        # Act
        test_client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        response_after = test_client.get("/activities")
        participants_after = response_after.json()[activity_name]["participants"]
        assert email in participants_after
    
    def test_signup_nonexistent_activity_returns_404(self, test_client, reset_activities):
        """
        Arrange: Set up test client with invalid activity name
        Act: Submit signup request to nonexistent activity
        Assert: Verify 404 status and appropriate error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "charlie@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_email_returns_400(self, test_client, reset_activities):
        """
        Arrange: Set up test client, first signup already exists
        Act: Attempt to signup same email to same activity
        Assert: Verify 400 status and duplicate signup error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_same_user_different_activity_succeeds(self, test_client, reset_activities):
        """
        Arrange: Set up test client with user already in one activity
        Act: Signup same user to different activity
        Assert: Verify signup succeeds (same user can be in multiple activities)
        """
        # Arrange
        existing_activity = "Chess Club"
        new_activity = "Soccer Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = test_client.post(
            f"/activities/{new_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        response_after = test_client.get("/activities")
        assert email in response_after.json()[new_activity]["participants"]
        assert email in response_after.json()[existing_activity]["participants"]
    
    def test_signup_to_full_activity_returns_400(self, test_client, reset_activities):
        """
        Arrange: Set up test client, manually fill activity to capacity
        Act: Attempt to signup when activity is full
        Assert: Verify 400 status and full activity error
        """
        # Arrange
        activity_name = "Basketball Team"
        max_participants = 15
        
        # Fill the activity to capacity
        for i in range(max_participants):
            email = f"student{i}@mergington.edu"
            test_client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Try to add one more
        new_email = "overflow@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"]
    
    def test_signup_updates_availability_count(self, test_client, reset_activities):
        """
        Arrange: Set up test client and get initial spots available
        Act: Submit signup request
        Assert: Verify spots available decreased by 1
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "diana@mergington.edu"
        
        response_before = test_client.get("/activities")
        initial_participants = len(response_before.json()[activity_name]["participants"])
        initial_spots = response_before.json()[activity_name]["max_participants"] - initial_participants
        
        # Act
        test_client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        response_after = test_client.get("/activities")
        final_participants = len(response_after.json()[activity_name]["participants"])
        final_spots = response_after.json()[activity_name]["max_participants"] - final_participants
        
        assert final_participants == initial_participants + 1
        assert final_spots == initial_spots - 1
