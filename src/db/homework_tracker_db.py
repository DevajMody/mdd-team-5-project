# from swen610_db_utils import *
from src.db.swen610_db_utils import *
from psycopg2 import sql
import hashlib
import uuid
from datetime import datetime


def generate_session_key():
    """Generates a unique session key."""
    return str(uuid.uuid4())


def update_session_key(user_id, session_key):
    conn = connect()
    cur = conn.cursor()
    query = """
    UPDATE users
    SET session_key = %s
    WHERE user_id = %s
    """
    cur.execute(query, (session_key, user_id))
    conn.commit()
    conn.close()


def clear_session_key(user_id):
    conn = connect()
    cur = conn.cursor()
    query = """
    UPDATE users
    SET session_key = NULL
    WHERE user_id = %s
    """
    cur.execute(query, (user_id,))
    conn.commit()
    conn.close()


def get_user_by_session_key(session_key):
    conn = connect()
    cur = conn.cursor()
    query = """
    SELECT user_id, user_name, email
    FROM users
    WHERE session_key = %s
    """
    cur.execute(query, (session_key,))
    user = cur.fetchone()
    conn.close()
    if user:
        return {"user_id": user[0], "user_name": user[1], "email": user[2]}
    return None


def rebuild_tables():
    try:
        exec_sql_file("src/db/schema.sql")  # Ensure the correct path to schema.sql
        print("Tables rebuilt successfully")
    except Exception as e:
        print(f"Error in rebuild_tables: {e}")


def deleteTables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS users CASCADE")
    cur.execute("DROP TABLE IF EXISTS homework CASCADE")
    cur.execute("DROP TABLE IF EXISTS categories CASCADE")

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)


def signup(name, email, password):
    conn = connect()
    cur = conn.cursor()
    hashed_password = hash_password(password)
    query = """
    INSERT INTO users (user_name, email, password)
    VALUES (%s, %s, %s) RETURNING user_id
    """
    cur.execute(query, (name, email, hashed_password))
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id


def signin(email, password):
    conn = connect()
    cur = conn.cursor()
    query = """
    SELECT user_id, user_name, email, password, session_key
    FROM users
    WHERE email = %s
    """
    cur.execute(query, (email,))
    user = cur.fetchone()
    conn.close()
    if user and verify_password(user[3], password):
        if not user[4]:
            session_key = generate_session_key()
            update_session_key(user[0], session_key)
        else:
            session_key = user[4]
        return {
            "user_id": user[0],
            "user_name": user[1],
            "email": user[2],
            "session_key": session_key,
        }
    return None


def create_homework(user_id, title, description, due_date, priority="Normal"):
    conn = connect()
    cur = conn.cursor()
    try:
        # Validate input parameters
        if not user_id:
            raise ValueError("User ID is required")
        if not title:
            raise ValueError("Title is required")
        if not description:
            raise ValueError("Description is required")
        if not due_date:
            raise ValueError("Due date is required")

        # Print debug information
        print(f"Creating homework - User ID: {user_id}, Title: {title}")

        query = """
        INSERT INTO homework (user_id, title, description, created_date, due_date, is_completed, priority)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, false, %s) 
        RETURNING homework_id
        """
        cur.execute(query, (user_id, title, description, due_date, priority))
        homework_id = cur.fetchone()[0]
        conn.commit()

        print(f"Homework created successfully with ID: {homework_id}")
        return homework_id
    except Exception as e:
        conn.rollback()
        print(f"Detailed error in create_homework: {e}")
        # Re-raise with more context
        raise ValueError(f"Failed to create homework: {str(e)}")
    finally:
        cur.close()
        conn.close()


def delete_homework(homework_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM homework WHERE homework_id = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute("DELETE FROM homework WHERE homework_id = %s", (homework_id,))
    conn.commit()
    conn.close()
    return "Homework deleted successfully"


def edit_homework(
    homework_id,
    title=None,
    description=None,
    due_date=None,
    is_completed=None,
    priority=None,
):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM homework WHERE homework_id = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    update_fields = []
    update_values = []
    if title:
        update_fields.append("title = %s")
        update_values.append(title)
    if description:
        update_fields.append("description = %s")
        update_values.append(description)
    if due_date:
        update_fields.append("due_date = %s")
        update_values.append(due_date)
    if is_completed is not None:
        update_fields.append("is_completed = %s")
        update_values.append(is_completed)
    if priority:
        update_fields.append("priority = %s")
        update_values.append(priority)

    update_values.append(homework_id)
    cur.execute(
        sql.SQL("UPDATE homework SET {} WHERE homework_id = %s").format(
            sql.SQL(", ").join(map(sql.SQL, update_fields))
        ),
        update_values,
    )
    conn.commit()
    conn.close()
    return "Homework updated successfully"


def change_password(user_id, new_password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if not cur.fetchone():
        conn.close()
        return "User does not exist"

    hashed_password = hash_password(new_password)
    cur.execute(
        "UPDATE users SET password = %s WHERE user_id = %s", (hashed_password, user_id)
    )
    conn.commit()
    conn.close()
    return "Password changed successfully"


def get_user_data(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user_data = cur.fetchone()
    conn.close()
    return user_data if user_data else []


def view_homework(user_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        SELECT t.homework_id, t.user_id, t.title, t.description, t.category_id, 
               t.created_date, t.due_date, c.category_name, t.is_completed, t.priority
        FROM homework t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
        ORDER BY t.homework_id
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


def get_homework(homework_id):
    conn = connect()
    cur = conn.cursor()
    try:
        query = """
        SELECT t.homework_id, t.user_id, t.title, t.description, t.category_id, 
               t.created_date, t.due_date, c.category_name, t.is_completed,  t.priority
        FROM homework t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.homework_id = %s
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


def add_category(category_name):
    conn = connect()
    cur = conn.cursor()
    query = """
    INSERT INTO categories (category_name)
    VALUES (%s) RETURNING category_id
    """
    cur.execute(query, (category_name,))
    category_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return category_id


def delete_category(category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    if not cur.fetchone():
        conn.close()
        return "Category does not exist"

    cur.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()
    return "Category deleted successfully"


def assign_category(homework_id, category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM homework WHERE homework_id = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    if not cur.fetchone():
        conn.close()
        return "Category does not exist"

    cur.execute(
        "UPDATE homework SET category_id = %s WHERE homework_id = %s",
        (category_id, homework_id),
    )
    conn.commit()
    conn.close()
    return "Category assigned to homework successfully"


def remove_category(homework_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM homework WHERE homework_id = %s", (homework_id,))
    if not cur.fetchone():
        conn.close()
        return "Homework does not exist"

    cur.execute(
        "UPDATE homework SET category_id = NULL WHERE homework_id = %s", (homework_id,)
    )
    conn.commit()
    conn.close()
    return "Category removed from homework successfully"


def get_due_dates_from_db(user_id):
    """
    Fetch due dates for the given user ID from the database.

    Args:
        user_id (int): The ID of the user whose homework due dates are to be fetched.

    Returns:
        list[dict]: A list of homework due dates with `homework_id`, `title`, and `due_date`.
    """
    try:
        conn = connect()
        cur = conn.cursor()
        query = "SELECT homework_id, title, due_date FROM homework WHERE user_id = %s"
        cur.execute(query, (user_id,))
        homework = cur.fetchall()
        conn.close()

        # Format the result into a list of dictionaries
        result = []
        for hw in homework:
            result.append(
                {
                    "homework_id": hw[0],
                    "title": hw[1],
                    "due_date": hw[2],  # Keep the datetime object as is
                }
            )
        return result
    except Exception as e:
        raise Exception(f"Error fetching due dates: {e}")
