import unittest
from tests.test_utils import *


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Initialize DB using API call"""
        post_rest_call(self, "http://localhost:5000/manage/init")
        print("DB Should be reset now")

    def test_signup(self):
        """Test API for signing up a new user"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
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
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        response = post_rest_call(
            self,
            "http://localhost:5000/signin",
            json={"email": "john@example.com", "password": "password123"},
            expected_code=200,
        )
        self.assertIn("user", response, "User details not returned in response")

    def test_create_task(self):
        """Test API for creating a task"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_task = {
            "user_id": user_id,
            "title": "Test Task",
            "description": "This is a test task",
        }
        response = post_rest_call(
            self, "http://localhost:5000/tasks", json=new_task, expected_code=201
        )
        self.assertIn("task_id", response, "Task ID not returned in response")

    def test_delete_task(self):
        """Test API for deleting a task"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_task = {
            "user_id": user_id,
            "title": "Test Task",
            "description": "This is a test task",
        }
        task_response = post_rest_call(
            self, "http://localhost:5000/tasks", json=new_task, expected_code=201
        )
        task_id = task_response["task_id"]
        response = requests.delete(f"http://localhost:5000/tasks/{task_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete task")

    def test_edit_task(self):
        """Test API for editing a task"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_task = {
            "user_id": user_id,
            "title": "Test Task",
            "description": "This is a test task",
        }
        task_response = post_rest_call(
            self, "http://localhost:5000/tasks", json=new_task, expected_code=201
        )
        task_id = task_response["task_id"]
        updated_task = {
            "title": "Updated Task",
            "description": "This is an updated test task",
        }
        response = requests.put(
            f"http://localhost:5000/tasks/{task_id}", json=updated_task
        )
        self.assertEqual(response.status_code, 200, "Failed to update task")

    def test_add_category(self):
        """Test API for adding a category"""
        new_category = {"category_name": "Work"}
        response = post_rest_call(
            self,
            "http://localhost:5000/categories",
            json=new_category,
            expected_code=201,
        )
        self.assertIn("category_id", response, "Category ID not returned in response")

    def test_delete_category(self):
        """Test API for deleting a category"""
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:5000/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        response = requests.delete(f"http://localhost:5000/categories/{category_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete category")

    def test_assign_category(self):
        """Test API for assigning a category to a task"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_task = {
            "user_id": user_id,
            "title": "Test Task",
            "description": "This is a test task",
        }
        task_response = post_rest_call(
            self, "http://localhost:5000/tasks", json=new_task, expected_code=201
        )
        task_id = task_response["task_id"]
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:5000/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        response = requests.put(
            f"http://localhost:5000/tasks/{task_id}/category/{category_id}"
        )
        self.assertEqual(response.status_code, 200, "Failed to assign category to task")

    def test_remove_category(self):
        """Test API for removing a category from a task"""
        new_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        user_response = post_rest_call(
            self, "http://localhost:5000/signup", json=new_user, expected_code=201
        )
        user_id = user_response["user_id"]
        new_task = {
            "user_id": user_id,
            "title": "Test Task",
            "description": "This is a test task",
        }
        task_response = post_rest_call(
            self, "http://localhost:5000/tasks", json=new_task, expected_code=201
        )
        task_id = task_response["task_id"]
        new_category = {"category_name": "Work"}
        category_response = post_rest_call(
            self,
            "http://localhost:5000/categories",
            json=new_category,
            expected_code=201,
        )
        category_id = category_response["category_id"]
        requests.put(f"http://localhost:5000/tasks/{task_id}/category/{category_id}")
        response = requests.put(f"http://localhost:5000/tasks/{task_id}/category")
        self.assertEqual(
            response.status_code, 200, "Failed to remove category from task"
        )

    def tearDown(self):
        """Clean up the DB using API call"""
        post_rest_call(self, "http://localhost:5000/teardown")
        print("DB Should be deleted now")


if __name__ == "__main__":
    unittest.main()
