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

# Homework APIs
api.add_resource(CreateHomework, "/homework", endpoint="create_homework")
api.add_resource(DeleteHomework, "/homework/<int:homework_id>", endpoint="delete_homework")
api.add_resource(EditHomework, "/homework/<int:homework_id>", endpoint="edit_homework")
api.add_resource(ViewHomeworks, "/homework/user/<int:user_id>", endpoint="view_homework")
api.add_resource(GetHomework, "/homework/user/<int:homework_id>", endpoint="get_homework")

# Category APIs
api.add_resource(AddCategory, "/categories", endpoint="add_category")
api.add_resource(
    DeleteCategory, "/categories/<int:category_id>", endpoint="delete_category"
)
api.add_resource(
    AssignCategory,
    "/homework/<int:homework_id>/category/<int:category_id>",
    endpoint="assign_category",
)
api.add_resource(
    RemoveCategory, "/homework/<int:homework_id>/category", endpoint="remove_category"
)

if __name__ == "__main__":
    rebuild_tables()
    app.run(port=8001, debug=True)
