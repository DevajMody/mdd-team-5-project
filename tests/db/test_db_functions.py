import unittest
from datetime import datetime
from src.db.homework_tracker_db import *
from src.db.swen610_db_utils import connect


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Setup the test database and seed the data"""
        # Rebuild the tables in the test database
        rebuild_tables()

        # Add users to the Users table
        self.user1_id = signup("Alice", "alice@example.com", "password123")
        self.user2_id = signup("Bob", "bob@example.com", "password456")
        self.user3_id = signup("Charlie", "charlie@example.com", "password789")

        # Create tasks for users
        self.task1_id = create_task(
            self.user1_id, "Buy groceries", "Buy milk, eggs, and bread"
        )
        self.task2_id = create_task(self.user1_id, "Read book", "Finish reading '1984'")
        self.task3_id = create_task(self.user2_id, "Exercise", "Go for a 30-minute run")

    def test_signup(self):
        """Test user signup"""
        user_id = signup("David", "david@example.com", "password321")
        self.assertIsNotNone(user_id, "Signup should return a user ID")

    def test_signin(self):
        """Test user signin"""
        user = signin("alice@example.com", "password123")
        self.assertIsNotNone(user, "Signin should return user details")
        self.assertEqual(user[1], "Alice", "User name should be Alice")

    def test_create_task(self):
        """Test creating a task"""
        task_id = create_task(
            self.user3_id, "Clean house", "Vacuum and dust the living room"
        )
        self.assertIsNotNone(task_id, "Create task should return a task ID")

    def test_delete_task(self):
        """Test deleting a task"""
        response = delete_task(self.task1_id)
        self.assertEqual(
            response, "Task deleted successfully", "Should confirm task deletion"
        )

    def test_edit_task(self):
        """Test editing a task"""
        response = edit_task(
            self.task2_id,
            title="Read a book",
            description="Finish reading '1984' by George Orwell",
        )
        self.assertEqual(
            response, "Task updated successfully", "Should confirm task update"
        )

    def test_change_password(self):
        """Test changing user password"""
        response = change_password(self.user1_id, "newpassword123")
        self.assertEqual(
            response, "Password changed successfully", "Should confirm password change"
        )

    def test_get_user_data(self):
        """Test getting user data"""
        user_data = get_user_data(self.user1_id)
        self.assertIsNotNone(user_data, "Get user data should return user details")
        self.assertEqual(user_data[1], "Alice", "User name should be Alice")

    def test_view_tasks(self):
        """Test viewing tasks"""
        tasks = view_tasks(self.user1_id)
        self.assertEqual(len(tasks), 2, "User should have 2 tasks")
        self.assertEqual(
            tasks[0][2], "Buy groceries", "First task title should be 'Buy groceries'"
        )
        self.assertEqual(
            tasks[1][2], "Read book", "Second task title should be 'Read book'"
        )

    def test_add_category(self):
        """Test adding a category"""
        category_id = add_category("Work")
        self.assertIsNotNone(category_id, "Add category should return a category ID")

    def test_delete_category(self):
        """Test deleting a category"""
        category_id = add_category("Personal")
        response = delete_category(category_id)
        self.assertEqual(
            response,
            "Category deleted successfully",
            "Should confirm category deletion",
        )

    def test_assign_category(self):
        """Test assigning a category to a task"""
        category_id = add_category("Urgent")
        response = assign_category(self.task1_id, category_id)
        self.assertEqual(
            response,
            "Category assigned to task successfully",
            "Should confirm category assignment",
        )

    def test_remove_category(self):
        """Test removing a category from a task"""
        category_id = add_category("Optional")
        assign_category(self.task2_id, category_id)
        response = remove_category(self.task2_id)
        self.assertEqual(
            response,
            "Category removed from task successfully",
            "Should confirm category removal",
        )

    def tearDown(self):
        """Clean up the test database by deleting the tables"""
        deleteTables()


if __name__ == "__main__":
    unittest.main()
