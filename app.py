
import datetime
import enum
import uuid
from flask import Flask, render_template
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields


server = Flask(__name__)  # Create Flask application instance


class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone"


server.config.from_object(APIConfig)

api = Api(server)

todo = Blueprint("todo", "todo", url_prefix="/todo", description="TODO API")

tasks = [
    {
        "id": uuid.UUID("865d9d3b-f56b-47e4-ba71-246fe00ea74b"),
        "created": datetime.datetime.now(datetime.timezone.utc),
        "completed": False,
        "task": "Create Flask API tutorial",
    }
]


class CreateTask(Schema):
    task = fields.String()


class UpdateTask(CreateTask):
    completed = fields.Bool()


class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()


class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task))


class SortByEnum(enum.Enum):
    task = "task"
    created = "created"


class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


class ListTasksParameters(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.created)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)


@todo.route("/tasks")
class TodoCollection(MethodView):
    @todo.arguments(ListTasksParameters, location="query")
    # @todo.response(status_code=200, schema=ListTasks)
    def get(self, parameters):
        print(f"Tasks being passed to template: {tasks}")
        return render_template("tasks.html", tasks=tasks)

    @todo.arguments(CreateTask)
    @todo.response(status_code=201, schema=Task)
    def post(self, task):
        task["id"] = uuid.uuid4()
        task["created"] = datetime.datetime.now(datetime.timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task


api.register_blueprint(todo)


if __name__ == "__main__":
    server.run(debug=True)
