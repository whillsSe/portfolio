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

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

with app.app_context():
    db.create_all()
    print("dbChecked.")

