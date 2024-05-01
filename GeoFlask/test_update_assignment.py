import unittest
import requests
import jwt
from datetime import datetime
from utility.config import configuration
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


URLpre = configuration["URLpre"]  # "https://localhost:7042/api/v1/"

class TestUpdateAssignment(unittest.TestCase):

    def perform_login(self, email, password):
        """Performs user login and returns a JWT token or error."""
        data = {"GokstadEmail": email, "Password": password}
        url = URLpre + "login"
        response = requests.post(url, verify=False, json=data)
        if not response.ok:
            return None, "Could not log in."
        return response.text, None  # Use the JWT directly

    def setUp(self):
        """Set up test data or state before each test by ensuring a user is logged in and an assignment exists."""
        token, error = self.perform_login("johannes.andersen@gokstadakademiet.no", "MZHlhk54")
        if error or not token:
            self.fail(f"Setup failed with login error: {error}")
        self.token = token  # Store the token for use in other methods
        self.test_assignment_id = self.create_test_assignment()
        if not self.test_assignment_id:
            self.fail("Failed to create test assignment.")

    def create_test_assignment(self):
        """Helper function to create a test assignment and return its ID."""
        post_data = {
            "CourseImplementationId": 102,
            "Name": "Test Assignment",
            "Description": "Initial test assignment.",
            "Deadline": datetime.now().isoformat(),
            "Mandatory": False
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(URLpre + "assignments", json=post_data, headers=headers, verify=False)
        if response.ok:
            return response.json()['id']
        else:
            print(f"Failed to create assignment: Status Code: {response.status_code}, Response Body: {response.text}")
            return None

    def test_update_assignment(self):
        """Test the update functionality for an assignment using the created assignment ID."""
        url = URLpre + f"assignment/{self.test_assignment_id}"
        update_data = {
            "CourseImplementationId": 102,
            "Name": "Updated Assignment Name",
            "Description": "Updated Description with more details.",
            "Deadline": datetime.now().isoformat(),
            "Mandatory": False
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(url, json=update_data, headers=headers, verify=False)
        if response.status_code not in [200, 204]:
            print(f"Failed to update, response code {response.status_code}, response body: {response.text}")
        self.assertIn(response.status_code, [200, 204], f"Failed to update, response code {response.status_code}")

if __name__ == "__main__":
    unittest.main()
