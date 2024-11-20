from flask import Flask
from flask_restful import Api
from api.homework_tracker_api import *


app = Flask(__name__)
api = Api(app)

api.add_resource(Init, "/manage/init")  # Management API for initializing the DB

api.add_resource(Version, "/manage/version")  # Management API for checking DB version

api.add_resource(TearDown, "/teardown")

# User APIs
api.add_resource(SignUp, "/signup", endpoint="signup")
api.add_resource(SignIn, "/signin", endpoint="signin")
api.add_resource(
    ChangePassword, "/change_password/<int:user_id>", endpoint="change_password"
)
api.add_resource(GetUserData, "/user/<int:user_id>", endpoint="get_user_data")

# Task APIs
api.add_resource(CreateTask, "/tasks", endpoint="create_task")
api.add_resource(DeleteTask, "/tasks/<int:task_id>", endpoint="delete_task")
api.add_resource(EditTask, "/tasks/<int:task_id>", endpoint="edit_task")
api.add_resource(ViewTasks, "/tasks/user/<int:user_id>", endpoint="view_tasks")

# Category APIs
api.add_resource(AddCategory, "/categories", endpoint="add_category")
api.add_resource(
    DeleteCategory, "/categories/<int:category_id>", endpoint="delete_category"
)
api.add_resource(
    AssignCategory,
    "/tasks/<int:task_id>/category/<int:category_id>",
    endpoint="assign_category",
)
api.add_resource(
    RemoveCategory, "/tasks/<int:task_id>/category", endpoint="remove_category"
)

if __name__ == "__main__":
    rebuild_tables()
    app.run(debug=True)
