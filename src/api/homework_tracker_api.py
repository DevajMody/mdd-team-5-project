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


class CreateTask(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("title", required=True)
        parser.add_argument("description", required=True)
        args = parser.parse_args()

        try:
            task_id = create_task(args["user_id"], args["title"], args["description"])
            return {"task_id": task_id}, 201
        except Exception as e:
            return {"message": str(e)}, 400


class DeleteTask(Resource):
    def delete(self, task_id):
        response = delete_task(task_id)
        if response == "Task deleted successfully":
            return {"message": response}, 200
        return {"message": response}, 404


class EditTask(Resource):
    def put(self, task_id):
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        response = edit_task(task_id, title, description)
        if response == "Task updated successfully":
            return {"message": response}, 200
        return {"message": response}, 400


class ViewTasks(Resource):
    def get(self, user_id):
        tasks = view_tasks(user_id)
        task_list = []
        for task in tasks:
            task_dict = {
                "task_id": task[0],
                "user_id": task[1],
                "title": task[2],
                "description": task[3],
                "category_id": task[4],
                "created_date": str(task[5]) if task[5] else None,
                "category_name": task[6] if len(task) > 6 else None,
            }
            task_list.append(task_dict)
        return {"tasks": task_list}, 200


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
    def put(self, task_id, category_id):
        response = assign_category(task_id, category_id)
        if response == "Category assigned to task successfully":
            return {"message": response}, 200
        return {"message": response}, 400


class RemoveCategory(Resource):
    def put(self, task_id):
        response = remove_category(task_id)
        if response == "Category removed from task successfully":
            return {"message": response}, 200
        return {"message": response}, 400
