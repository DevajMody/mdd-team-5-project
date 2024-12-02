import unittest
import requests
from tests.test_utils import *


class TestHomeworkManager(unittest.TestCase):

    def setUp(self):
        """Initialize DB using API call"""
        self.session = requests.Session()  # Create a session for global headers
        post_rest_call(self, "http://localhost:8001/manage/init")
        print("DB Should be reset now")

    def test_signup(self):
        """Test API for signing up a new user"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        self.assertIn("user_id", response, "User ID not returned in response")

    def test_signin(self):
        """Test API for signing in a user"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        response = post_rest_call(
            self,
            "http://localhost:8001/signin",
            json={"email": "john@example.com", "password": "password123"},
            expected_code=200,
        )
        self.assertIn("user", response, "User details not returned in response")
        self.assertIn(
            "session_key", response["user"], "Session key not returned in response"
        )
        session_key = response["user"]["session_key"]
        self.assertIsNotNone(session_key, "Session key should not be None")

        # Set the session key in the global headers
        self.session.headers.update({"Session-Key": session_key})

    def test_create_homework(self):
        """Test API for creating a homework"""
        # Sign in first to get a session key
        self.test_signin()  # This will set the session key in self.session.headers

        # Extensive debug information
        print("Test Session Headers:", self.session.headers)
        print("Session Key:", self.session.headers.get("Session-Key"))

        new_homework = {
            "title": "Test Homework",
            "description": "This is a test homework",
            "due_date": "2024-12-01T12:00:00",
            "priority": "High",
        }

        # Use the session with the pre-set headers
        response = self.session.post(
            "http://localhost:8001/homework",
            json=new_homework,
        )

        # Comprehensive error reporting
        print("Create Homework Response Status:", response.status_code)
        print("Create Homework Response Headers:", response.headers)
        print("Create Homework Response Text:", response.text)

        try:
            response_data = response.json()
        except ValueError:
            print("Failed to parse JSON response")
            response_data = {}

        self.assertEqual(
            response.status_code,
            201,
            f"Failed to create homework. Status: {response.status_code}, Response: {response.text}",
        )

        self.assertIn(
            "homework_id", response_data, "Homework ID not returned in response"
        )

    def test_delete_homework(self):
        """Test API for deleting a homework"""
        self.test_create_homework()  # Create a homework to delete
        response = self.session.delete(
            "http://localhost:8001/homework/1"  # Assuming ID 1 for the created homework
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Failed to delete homework. Response: {response.text}",
        )

    def test_edit_homework(self):
        """Test API for editing a homework"""
        self.test_create_homework()  # Create a homework to edit
        updated_homework = {
            "title": "Updated Homework",
            "description": "This is an updated test homework",
            "due_date": "2024-12-10T12:00:00",
            "priority": "Normal",
        }
        response = self.session.put(
            "http://localhost:8001/homework/1",  # Assuming ID 1 for the created homework
            json=updated_homework,
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Failed to update homework. Response: {response.text}",
        )

    def test_add_category(self):
        """Test API for adding a category"""
        self.test_signin()  # Sign in and set session key
        new_category = {"category_name": "Work"}
        response = self.session.post(
            "http://localhost:8001/categories",
            json=new_category,
        )
        self.assertEqual(response.status_code, 201, "Failed to add category")
        response_data = response.json()
        self.assertIn(
            "category_id", response_data, "Category ID not returned in response"
        )

    def test_assign_category(self):
        """Test API for assigning a category to a homework"""
        # Sign up a user first
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        signup_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )

        # Sign in the user to get a session key
        signin_response = post_rest_call(
            self,
            "http://localhost:8001/signin",
            json={"email": "john@example.com", "password": "password123"},
            expected_code=200,
        )
        session_key = signin_response["user"]["session_key"]
        self.session.headers.update({"Session-Key": session_key})

        # Create a homework
        new_homework = {
            "title": "Test Homework",
            "description": "This is a test homework",
            "due_date": "2024-12-01T12:00:00",
            "priority": "High",
        }
        homework_response = self.session.post(
            "http://localhost:8001/homework",
            json=new_homework,
        )
        self.assertEqual(
            homework_response.status_code,
            201,
            f"Failed to create homework. Response: {homework_response.text}",
        )
        homework_id = homework_response.json()["homework_id"]

        # Add a category
        new_category = {"category_name": "Work"}
        category_response = self.session.post(
            "http://localhost:8001/categories",
            json=new_category,
        )
        self.assertEqual(
            category_response.status_code,
            201,
            f"Failed to add category. Response: {category_response.text}",
        )
        category_id = category_response.json()["category_id"]

        # Assign category to homework
        assign_response = self.session.put(
            f"http://localhost:8001/homework/{homework_id}/category/{category_id}"
        )
        self.assertEqual(
            assign_response.status_code,
            200,
            f"Failed to assign category to homework. Response: {assign_response.text}",
        )

    def test_remove_category(self):
        """Test API for removing a category from a homework"""
        # Sign up a user first
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        signup_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )

        # Sign in the user to get a session key
        signin_response = post_rest_call(
            self,
            "http://localhost:8001/signin",
            json={"email": "john@example.com", "password": "password123"},
            expected_code=200,
        )
        session_key = signin_response["user"]["session_key"]
        self.session.headers.update({"Session-Key": session_key})

        # Create a homework
        new_homework = {
            "title": "Test Homework",
            "description": "This is a test homework",
            "due_date": "2024-12-01T12:00:00",
            "priority": "Normal",
        }
        homework_response = self.session.post(
            "http://localhost:8001/homework",
            json=new_homework,
        )
        self.assertEqual(
            homework_response.status_code,
            201,
            f"Failed to create homework. Response: {homework_response.text}",
        )
        homework_id = homework_response.json()["homework_id"]

        # Add a category
        new_category = {"category_name": "Work"}
        category_response = self.session.post(
            "http://localhost:8001/categories",
            json=new_category,
        )
        self.assertEqual(
            category_response.status_code,
            201,
            f"Failed to add category. Response: {category_response.text}",
        )
        category_id = category_response.json()["category_id"]

        # Assign category to homework
        assign_response = self.session.put(
            f"http://localhost:8001/homework/{homework_id}/category/{category_id}"
        )
        self.assertEqual(
            assign_response.status_code,
            200,
            f"Failed to assign category to homework. Response: {assign_response.text}",
        )

        # Remove category from homework
        remove_response = self.session.put(
            f"http://localhost:8001/homework/{homework_id}/category"
        )
        self.assertEqual(
            remove_response.status_code,
            200,
            f"Failed to remove category from homework. Response: {remove_response.text}",
        )

    def tearDown(self):
        """Clean up the DB using API call"""
        post_rest_call(self, "http://localhost:8001/teardown")
        print("DB Should be deleted now")


if __name__ == "__main__":
    unittest.main()
