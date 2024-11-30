from flask_restful import Resource, request, reqparse
from db.swen610_db_utils import *
from db.homework_tracker_db import *
from db.homework_tracker_db import rebuild_tables, deleteTables
import traceback


class Init(Resource):
    def post(self):
        rebuild_tables()


class Version(Resource):
    def get(self):
        return exec_get_one("SELECT VERSION()")


class TearDown(Resource):
    def post(self):
        deleteTables()


class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)  # Force parsing even if content-type is not set
            print("Received data:", data)  # Debug log
            
            if not data:
                print("No data received")
                return {"message": "No data provided"}, 400

            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            # More detailed validation
            if not all([name, email, password]):
                print("Missing fields:", {"name": name, "email": email, "password": bool(password)})
                return {"message": "Missing required fields"}, 400

            user_id = signup(name, email, password)
            return {"user_id": user_id}, 201

        except Exception as e:
            print(f"Signup Error: {str(e)}")
            print(traceback.format_exc())
            return {"message": f"Internal server error: {str(e)}"}, 500




class SignIn(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = signin(email, password)
        if user:
            return {"user": user}, 200
        return {"message": "Invalid credentials"}, 401


class Logout(Resource):
    def post(self):
        session_key = request.headers.get("Session-Key")

        if not session_key:
            return {"message": "Session key is required"}, 400

        # Fetch the user associated with the session key
        user = get_user_by_session_key(session_key)
        if not user:
            return {"message": "Invalid session key"}, 401

        try:
            # Clear the session key from the database
            clear_session_key(user["user_id"])
            return {"message": "Logged out successfully"}, 200
        except Exception as e:
            return {"message": f"Error during logout: {str(e)}"}, 500



class ChangePassword(Resource):
    def put(self, user_id):
        data = request.get_json()
        new_password = data.get("new_password")
        response = change_password(user_id, new_password)
        if response == "Password changed successfully":
            return {"message": response}, 200
        return {"message": response}, 400


class GetUserData(Resource):
    def get(self, user_id):
        session_key = request.headers.get("Session-Key")

        if not session_key:
            return {"message": "Session key is required"}, 401

        user = get_user_by_session_key(session_key)
        if not user:
            return {"message": "Invalid session key"}, 401

        return {"user_data": user}, 200



class CreateHomework(Resource):
    def post(self):
        session_key = request.headers.get("Session-Key")
        if not session_key:
            return {"message": "Session key is required"}, 401

        user = get_user_by_session_key(session_key)
        if not user:
            return {"message": "Invalid session key or user not found"}, 401

        # Detailed debug print
        print("Full User Object:", user)
        print("Session Key Used:", session_key)

        # Explicitly extract user_id
        user_id = user.get("user_id")
        if not user_id:
            return {"message": "Could not extract valid UserID"}, 400

        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True, help="Title is required")
        parser.add_argument("description", required=True, help="Description is required")
        parser.add_argument("due_date", required=True, help="Due date is required")
        
        try:
            args = parser.parse_args()
        except Exception as parse_error:
            print(f"Parsing Error: {parse_error}")
            return {"message": str(parse_error)}, 400

        try:
            # Ensure due_date is in a valid format if needed
            homework_id = create_homework(
                user_id, 
                args["title"], 
                args["description"], 
                args["due_date"]
            )
            return {"homework_id": homework_id}, 201
        except Exception as e:
            print(f"Homework Creation Error: {str(e)}")
            return {"message": str(e)}, 400


class DeleteHomework(Resource):
    def delete(self, homework_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        response = delete_homework(homework_id)
        if response == "Homework deleted successfully":
            return {"message": response}, 200
        return {"message": response}, 404



class EditHomework(Resource):
    def put(self, homework_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")

        response = edit_homework(homework_id, title, description, due_date)
        if response == "Homework updated successfully":
            return {"message": response}, 200
        return {"message": response}, 400



class ViewHomeworks(Resource):
    def get(self, user_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        homework = view_homework(user_id)
        homework_list = []
        for hw in homework:
            homework_dict = {
                "homework_id": hw[0],
                "user_id": hw[1],
                "title": hw[2],
                "description": hw[3],
                "category_id": hw[4],
                "created_date": str(hw[5]) if hw[5] else None,
                "due_date": str(hw[6]) if hw[6] else None,
                "category_name": hw[7] if len(hw) > 7 else None,
            }
            homework_list.append(homework_dict)
        return {"homework": homework_list}, 200


    
    
class GetHomework(Resource):
    def get(self, homework_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        homework = get_homework(homework_id)
        if not homework:
            return {"message": "Homework not found"}, 404

        homework_dict = {
            "homework_id": homework[0],
            "user_id": homework[1],
            "title": homework[2],
            "description": homework[3],
            "category_id": homework[4],
            "created_date": str(homework[5]) if homework[5] else None,
            "due_date": str(homework[6]) if homework[6] else None,
            "category_name": homework[7] if len(homework) > 7 else None,
        }
        return {"homework": homework_dict}, 200



class AddCategory(Resource):
    def post(self):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        data = request.get_json()
        category_name = data.get("category_name")
        category_id = add_category(category_name)
        return {"category_id": category_id}, 201



class DeleteCategory(Resource):
    def delete(self, category_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        response = delete_category(category_id)
        if response == "Category deleted successfully":
            return {"message": response}, 200
        return {"message": response}, 404


class AssignCategory(Resource):
    def put(self, homework_id, category_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        response = assign_category(homework_id, category_id)
        if response == "Category assigned to homework successfully":
            return {"message": response}, 200
        return {"message": response}, 400



class RemoveCategory(Resource):
    def put(self, homework_id):
        session_key = request.headers.get("Session-Key")
        user = get_user_by_session_key(session_key)

        if not user:
            return {"message": "Unauthorized. Please log in."}, 401

        response = remove_category(homework_id)
        if response == "Category removed from homework successfully":
            return {"message": response}, 200
        return {"message": response}, 400
