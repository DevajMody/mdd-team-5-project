import unittest
from tests.test_utils import *


class TestHomeworkManager(unittest.TestCase):

    def setUp(self):
        """Initialize DB using API call"""
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

    def test_create_homework(self):
        """Test API for creating a homework"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_homework = {
            "user_id": user_id,
            "title": "Test Homework",
            "description": "This is a test homework",
            "due_date": "2024-12-01T12:00:00"  # Added due_date field
        }
        response = post_rest_call(
            self, "http://localhost:8001/homework", json=new_homework, expected_code=201
        )
        self.assertIn("homework_id", response, "Homework ID not returned in response")

    def test_delete_homework(self):
        """Test API for deleting a homework"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_homework = {
            "user_id": user_id,
            "title": "Test Homework",
            "description": "This is a test homework",
        }
        homework_response = post_rest_call(
            self, "http://localhost:8001/homework", json=new_homework, expected_code=201
        )
        homework_id = homework_response["homework_id"]
        response = requests.delete(f"http://localhost:8001/homework/{homework_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete homework")

    def test_edit_homework(self):
        """Test API for editing a homework"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_homework = {
            "user_id": user_id,
            "title": "Test Homework",
            "description": "This is a test homework",
            "due_date": "2024-12-01T12:00:00"  # Added due_date field
        }
        homework_response = post_rest_call(
            self, "http://localhost:8001/homework", json=new_homework, expected_code=201
        )
        homework_id = homework_response["homework_id"]
        updated_homework = {
            "title": "Updated Homework",
            "description": "This is an updated test homework",
            "due_date": "2024-12-10T12:00:00"  # Added due_date field for updating
        }
        response = requests.put(
            f"http://localhost:8001/homework/{homework_id}", json=updated_homework
        )
        self.assertEqual(response.status_code, 200, "Failed to update homework")

    def test_add_category(self):
        """Test API for adding a category"""
        new_category = {"category_name": "Work"}
        response = post_rest_call(
            self,
            "http://localhost:8001/categories",
            json=new_category,
            expected_code=201,
        )
        self.assertIn("category_id", response, "Category ID not returned in response")

    def test_delete_category(self):
        """Test API for deleting a category"""
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:8001/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        response = requests.delete(f"http://localhost:8001/categories/{category_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete category")

    def test_assign_category(self):
        """Test API for assigning a category to a homework"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_homework = {
            "user_id": user_id,
            "title": "Test Homework",
            "description": "This is a test homework",
        }
        homework_response = post_rest_call(
            self, "http://localhost:8001/homework", json=new_homework, expected_code=201
        )
        homework_id = homework_response["homework_id"]
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:8001/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        response = requests.put(
            f"http://localhost:8001/homework/{homework_id}/category/{category_id}"
        )
        self.assertEqual(response.status_code, 200, "Failed to assign category to homework")

    def test_remove_category(self):
        """Test API for removing a category from a homework"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:8001/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_homework = {
            "user_id": user_id,
            "title": "Test Homework",
            "description": "This is a test homework",
        }
        homework_response = post_rest_call(
            self, "http://localhost:8001/homework", json=new_homework, expected_code=201
        )
        homework_id = homework_response["homework_id"]
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:8001/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        requests.put(f"http://localhost:8001/homework/{homework_id}/category/{category_id}")
        response = requests.put(f"http://localhost:8001/homework/{homework_id}/category")
        self.assertEqual(
            response.status_code, 200, "Failed to remove category from homework"
        )

    def tearDown(self):
        """Clean up the DB using API call"""
        post_rest_call(self, "http://localhost:8001/teardown")
        print("DB Should be deleted now")


if __name__ == "__main__":
    unittest.main()
