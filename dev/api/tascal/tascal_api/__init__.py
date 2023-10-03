from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

import settings
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = settings.PRIVATE_KEY #デプロイ時はdockerの環境変数から読み込む
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_ECHO'] = settings.DB_ECHO
app.config['SERVER_NAME'] = settings.SERVER_NAME

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from tascal_api.resources.tasks import TaskResource
from tascal_api.resources.task_item import TaskItemResource
from tascal_api.resources.task_complete import TaskComplete
from tascal_api.resources.task_uncomplete import TaskUncomplete

with app.app_context():
    db.create_all()
    print("dbChecked.")

api.add_resource(TaskResource,'/tasks')
api.add_resource(TaskItemResource,'/tasks/<string:id>')
api.add_resource(TaskComplete,'/tasks/<string:id>/complete')
api.add_resource(TaskUncomplete,'/tasks/<string:id>/uncomplete')