from flask_restful import Resource, request, reqparse
from db.swen610_db_utils import *
from db.homework_tracker_db import *
from db.homework_tracker_db import rebuild_tables, deleteTables


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
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        user_id = signup(name, email, password)
        return {"user_id": user_id}, 201


class SignIn(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = signin(email, password)
        if user:
            return {"user": user}, 200
        return {"message": "Invalid credentials"}, 401


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
        user_data = get_user_data(user_id)
        if user_data:
            return {"user_data": user_data}, 200
        return {"message": "User not found"}, 404


class CreateHomework(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("title", required=True)
        parser.add_argument("description", required=True)
        parser.add_argument("due_date", required=True)  # Added due_date argument
        args = parser.parse_args()

        try:
            homework_id = create_homework(args["user_id"], args["title"], args["description"], args["due_date"])
            return {"homework_id": homework_id}, 201
        except Exception as e:
            return {"message": str(e)}, 400


class DeleteHomework(Resource):
    def delete(self, homework_id):
        response = delete_homework(homework_id)
        if response == "Homework deleted successfully":
            return {"message": response}, 200
        return {"message": response}, 404


class EditHomework(Resource):
    def put(self, homework_id):
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")  # Added due_date

        response = edit_homework(homework_id, title, description, due_date)
        if response == "Homework updated successfully":
            return {"message": response}, 200
        return {"message": response}, 400


class ViewHomeworks(Resource):
    def get(self, user_id):
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
                "due_date": str(hw[6]) if hw[6] else None,  # Added due_date field
                "category_name": hw[7] if len(hw) > 7 else None,
            }
            homework_list.append(homework_dict)
        return {"homework": homework_list}, 200
    
    
class GetHomework(Resource):
    def get(self, homework_id):
        homework = get_homework(homework_id)
        homework_dict = {
            "homework_id": homework[0],
            "user_id": homework[1],
            "title": homework[2],
            "description": homework[3],
            "category_id": homework[4],
            "created_date": str(homework[5]) if homework[5] else None,
            "due_date": str(homework[6]) if homework[6] else None,  # Added due_date field
            "category_name": homework[7] if len(homework) > 7 else None,
        }
        return {"homework": homework_dict}, 200


class AddCategory(Resource):
    def post(self):
        data = request.get_json()
        category_name = data.get("category_name")
        category_id = add_category(category_name)
        return {"category_id": category_id}, 201


class DeleteCategory(Resource):
    def delete(self, category_id):
        response = delete_category(category_id)
        if response == "Category deleted successfully":
            return {"message": response}, 200
        return {"message": response}, 404


class AssignCategory(Resource):
    def put(self, homework_id, category_id):
        response = assign_category(homework_id, category_id)
        if response == "Category assigned to homework successfully":
            return {"message": response}, 200
        return {"message": response}, 400


class RemoveCategory(Resource):
    def put(self, homework_id):
        response = remove_category(homework_id)
        if response == "Category removed from homework successfully":
            return {"message": response}, 200
        return {"message": response}, 400
