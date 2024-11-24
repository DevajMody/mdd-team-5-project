import unittest
from datetime import datetime
from src.db.homework_tracker_db import *
from src.db.swen610_db_utils import connect


class TestHomeworkManager(unittest.TestCase):

    def setUp(self):
        """Setup the test database and seed the data"""
        # Rebuild the tables in the test database
        rebuild_tables()

        # Add users to the Users table
        self.user1_id = signup("Alice", "alice@example.com", "password123")
        self.user2_id = signup("Bob", "bob@example.com", "password456")
        self.user3_id = signup("Charlie", "charlie@example.com", "password789")

        # Create homework for users
        self.homework1_id = create_homework(
            self.user1_id, "Create repo", "Push db connector code"
        )
        self.homework2_id = create_homework(self.user1_id, "Setup database", "Make tables")
        self.homework3_id = create_homework(self.user2_id, "Setup API base", "Make routes")

    def test_signup(self):
        """Test user signup"""
        user_id = signup("David", "david@example.com", "password321")
        self.assertIsNotNone(user_id, "Signup should return a user ID")

    def test_signin(self):
        """Test user signin"""
        user = signin("alice@example.com", "password123")
        self.assertIsNotNone(user, "Signin should return user details")
        self.assertEqual(user[1], "Alice", "User name should be Alice")

    def test_create_homework(self):
        """Test creating a homework"""
        homework_id = create_homework(
            self.user3_id, "Design DB schema", "Insert test data"
        )
        self.assertIsNotNone(homework_id, "Create homework should return a homework ID")

    def test_delete_homework(self):
        """Test deleting a homework"""
        response = delete_homework(self.homework1_id)
        self.assertEqual(
            response, "Homework deleted successfully", "Should confirm homework deletion"
        )

    def test_edit_homework(self):
        """Test editing a homework"""
        response = edit_homework(
            self.homework2_id,
            title="Setup database",
            description="Make tables",
        )
        self.assertEqual(
            response, "Homework updated successfully", "Should confirm homework update"
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

    def test_view_homeworks(self):
        """Test viewing homework"""
        homework = view_homework(self.user1_id)
        self.assertEqual(len(homework), 2, "User should have 2 homework")
        self.assertEqual(
            homework[0][2], "Create repo", "First homework title should be 'Create repo'"
        )
        self.assertEqual(
            homework[1][2], "Setup database", "Second homework title should be 'Setup database'"
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
        """Test assigning a category to a homework"""
        category_id = add_category("Urgent")
        response = assign_category(self.homework1_id, category_id)
        self.assertEqual(
            response,
            "Category assigned to homework successfully",
            "Should confirm category assignment",
        )

    def test_remove_category(self):
        """Test removing a category from a homework"""
        category_id = add_category("Optional")
        assign_category(self.homework2_id, category_id)
        response = remove_category(self.homework2_id)
        self.assertEqual(
            response,
            "Category removed from homework successfully",
            "Should confirm category removal",
        )

    def tearDown(self):
        """Clean up the test database by deleting the tables"""
        deleteTables()


if __name__ == "__main__":
    unittest.main()
