from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

import settings 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = settings.PRIVATE_KEY #デプロイ時はdockerの環境変数から読み込む
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Change this to True for production
app.config['JWT_COOKIE_CSRF_PROTECT'] = False


api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
