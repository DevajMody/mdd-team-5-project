from .swen610_db_utils import *
from psycopg2 import sql
import hashlib


# Function to rebuild tables
def rebuild_tables():
    exec_sql_file("src/db/schema.sql")
    # exec_sql_file("src/db/taskmanager_data.sql")


# Function to drop tables
def deleteTables():
    conn = connect()
    cur = conn.cursor()

    dropUsers = "DROP TABLE IF EXISTS Users CASCADE"
    dropTasks = "DROP TABLE IF EXISTS Tasks CASCADE"
    dropCategories = "DROP TABLE IF EXISTS Categories CASCADE"

    cur.execute(dropUsers)
    cur.execute(dropTasks)
    cur.execute(dropCategories)

    conn.commit()
    conn.close()


# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to verify a password
def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)


# Function to signup a user
def signup(name, email, password):
    conn = connect()
    cur = conn.cursor()
    hashed_password = hash_password(password)
    query = """
    INSERT INTO Users (UserName, Email, Password)
    VALUES (%s, %s, %s) RETURNING UserID
    """
    cur.execute(query, (name, email, hashed_password))
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id


# Function to signin a user
def signin(email, password):
    conn = connect()
    cur = conn.cursor()
    query = """
    SELECT * FROM Users WHERE Email = %s
    """
    cur.execute(query, (email,))
    user = cur.fetchone()
    conn.close()
    if user and verify_password(user[3], password):
        return user
    return None


# Function to create a task
def create_task(user_id, title, description):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        INSERT INTO Tasks (UserID, Title, Description, CreatedDate)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP) 
        RETURNING TaskID
        """
        cur.execute(query, (user_id, title, description))
        task_id = cur.fetchone()[0]
        conn.commit()
        return task_id
    except Exception as e:
        conn.rollback()
        print(f"Error in create_task: {e}")
        raise
    finally:
        cur.close()
        conn.close()


# Function to delete a task
def delete_task(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks WHERE TaskID = %s", (task_id,))
    if not cur.fetchone():
        conn.close()
        return "Task does not exist"

    cur.execute("DELETE FROM Tasks WHERE TaskID = %s", (task_id,))
    conn.commit()
    conn.close()
    return "Task deleted successfully"


# Function to edit a task
def edit_task(task_id, title=None, description=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks WHERE TaskID = %s", (task_id,))
    if not cur.fetchone():
        conn.close()
        return "Task does not exist"

    update_fields = []
    update_values = []
    if title:
        update_fields.append("Title = %s")
        update_values.append(title)
    if description:
        update_fields.append("Description = %s")
        update_values.append(description)

    update_values.append(task_id)
    cur.execute(
        sql.SQL("UPDATE Tasks SET {} WHERE TaskID = %s").format(
            sql.SQL(", ").join(map(sql.SQL, update_fields))
        ),
        update_values,
    )
    conn.commit()
    conn.close()
    return "Task updated successfully"


# Function to change password
def change_password(user_id, new_password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
    if not cur.fetchone():
        conn.close()
        return "User does not exist"

    hashed_password = hash_password(new_password)
    cur.execute(
        "UPDATE Users SET Password = %s WHERE UserID = %s", (hashed_password, user_id)
    )
    conn.commit()
    conn.close()
    return "Password changed successfully"


# Function to get user data
def get_user_data(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
    user_data = cur.fetchone()
    conn.close()
    return user_data if user_data else []


# Function to view tasks
def view_tasks(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        SELECT t.TaskID, t.UserID, t.Title, t.Description, t.CategoryID, 
               t.CreatedDate, c.CategoryName
        FROM Tasks t
        LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
        WHERE t.UserID = %s
        ORDER BY t.TaskID
        """
        cur.execute(query, (user_id,))
        tasks = cur.fetchall()
        return tasks if tasks else []
    except Exception as e:
        print(f"Error in view_tasks: {e}")
        return []
    finally:
        cur.close()
        conn.close()


# Function to add a category
def add_category(category_name):
    conn = connect()
    cur = conn.cursor()
    query = """
    INSERT INTO Categories (CategoryName)
    VALUES (%s) RETURNING CategoryID
    """
    cur.execute(query, (category_name,))
    category_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return category_id


# Function to delete a category
def delete_category(category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Categories WHERE CategoryID = %s", (category_id,))
    if not cur.fetchone():
        conn.close()
        return "Category does not exist"

    cur.execute("DELETE FROM Categories WHERE CategoryID = %s", (category_id,))
    conn.commit()
    conn.close()
    return "Category deleted successfully"


# Function to assign or reassign a category to a task
def assign_category(task_id, category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks WHERE TaskID = %s", (task_id,))
    if not cur.fetchone():
        conn.close()
        return "Task does not exist"

    cur.execute("SELECT * FROM Categories WHERE CategoryID = %s", (category_id,))
    if not cur.fetchone():
        conn.close()
        return "Category does not exist"

    cur.execute(
        "UPDATE Tasks SET CategoryID = %s WHERE TaskID = %s", (category_id, task_id)
    )
    conn.commit()
    conn.close()
    return "Category assigned to task successfully"


# Function to remove the category from a task
def remove_category(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks WHERE TaskID = %s", (task_id,))
    if not cur.fetchone():
        conn.close()
        return "Task does not exist"

    cur.execute("UPDATE Tasks SET CategoryID = NULL WHERE TaskID = %s", (task_id,))
    conn.commit()
    conn.close()
    return "Category removed from task successfully"
