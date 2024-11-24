from .swen610_db_utils import *
from psycopg2 import sql
import hashlib


# Function to rebuild tables
def rebuild_tables():
    exec_sql_file("src/db/schema.sql")
    # exec_sql_file("src/db/homeworkmanager_data.sql")


# Function to drop tables
def deleteTables():
    conn = connect()
    cur = conn.cursor()

    dropUsers = "DROP TABLE IF EXISTS Users CASCADE"
    dropHomeworks = "DROP TABLE IF EXISTS Homework CASCADE"
    dropCategories = "DROP TABLE IF EXISTS Categories CASCADE"

    cur.execute(dropUsers)
    cur.execute(dropHomeworks)
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


# Function to create a homework
def create_homework(user_id, title, description, due_date):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        INSERT INTO Homework (UserID, Title, Description, CreatedDate, DueDate)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s) 
        RETURNING HomeworkID
        """
        cur.execute(query, (user_id, title, description, due_date))
        homework_id = cur.fetchone()[0]
        conn.commit()
        return homework_id
    except Exception as e:
        conn.rollback()
        print(f"Error in create_homework: {e}")
        raise
    finally:
        cur.close()
        conn.close()


# Function to delete a homework
def delete_homework(homework_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Homework WHERE HomeworkID = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute("DELETE FROM Homework WHERE HomeworkID = %s", (homework_id,))
    conn.commit()
    conn.close()
    return "Homework deleted successfully"


# Function to edit a homework
def edit_homework(homework_id, title=None, description=None, due_date=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Homework WHERE HomeworkID = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    update_fields = []
    update_values = []
    if title:
        update_fields.append("Title = %s")
        update_values.append(title)
    if description:
        update_fields.append("Description = %s")
        update_values.append(description)
    if due_date:
        update_fields.append("DueDate = %s")
        update_values.append(due_date)

    update_values.append(homework_id)
    cur.execute(
        sql.SQL("UPDATE Homework SET {} WHERE HomeworkID = %s").format(
            sql.SQL(", ").join(map(sql.SQL, update_fields))
        ),
        update_values,
    )
    conn.commit()
    conn.close()
    return "Homework updated successfully"


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


# Function to view homework
def view_homework(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        SELECT t.HomeworkID, t.UserID, t.Title, t.Description, t.CategoryID, 
               t.CreatedDate, t.DueDate, c.CategoryName
        FROM Homework t
        LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
        WHERE t.UserID = %s
        ORDER BY t.HomeworkID
        """
        cur.execute(query, (user_id,))
        homework = cur.fetchall()
        return homework if homework else []
    except Exception as e:
        print(f"Error in view_homework: {e}")
        return []
    finally:
        cur.close()
        conn.close()
        
# Function to view a specific homework
def get_homework(homework_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        SELECT t.HomeworkID, t.UserID, t.Title, t.Description, t.CategoryID, 
               t.CreatedDate, t.DueDate, c.CategoryName
        FROM Homework t
        LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
        WHERE t.HomeworkID = %s
        """
        cur.execute(query, (homework_id,))
        homework = cur.fetchall()
        return homework if homework else []
    except Exception as e:
        print(f"Error in get_homework: {e}")
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


# Function to assign or reassign a category to a homework
def assign_category(homework_id, category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Homework WHERE HomeworkID = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute("SELECT * FROM Categories WHERE CategoryID = %s", (category_id,))
    if not cur.fetchone():
        conn.close()
        return "Category does not exist"

    cur.execute(
        "UPDATE Homework SET CategoryID = %s WHERE HomeworkID = %s", (category_id, homework_id)
    )
    conn.commit()
    conn.close()
    return "Category assigned to homework successfully"


# Function to remove the category from a homework
def remove_category(homework_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Homework WHERE HomeworkID = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute("UPDATE Homework SET CategoryID = NULL WHERE HomeworkID = %s", (homework_id,))
    conn.commit()
    conn.close()
    return "Category removed from homework successfully"
