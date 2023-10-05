import time
from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from pymysql import OperationalError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

import settings
app = Flask(__name__)

app.config['JWT_PUBLIC_KEY'] = settings.PUBLIC_KEY #デプロイ時はdockerの環境変数から読み込む
app.config['JWT_ALGORITHM'] = settings.JWT_ALGORITHM
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

def try_db_connection():
    retries = 5
    while retries:
        try:
            db.session.query(text("1")).from_statement(text("SELECT 1")).all()
            print("DB connection established!")
            return
        except OperationalError as e:
            retries -= 1
            print(f"DB connection attempt failed. Retries left: {retries}")
            time.sleep(5)  # Wait for 5 seconds before retrying
    print("Could not connect to the database. Exiting...")
    exit(1)

with app.app_context():
    try_db_connection()
    db.create_all()
    print("dbChecked.")

api.add_resource(TaskResource,'/tasks')
api.add_resource(TaskItemResource,'/tasks/<string:id>')
api.add_resource(TaskComplete,'/tasks/<string:id>/complete')
api.add_resource(TaskUncomplete,'/tasks/<string:id>/uncomplete')