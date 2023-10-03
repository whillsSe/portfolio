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
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Change this to True for production
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_ECHO'] = settings.DB_ECHO
app.config['SERVER_NAME'] = settings.SERVER_NAME

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from tascal_auth.resources.authentication import AuthenticationResource
from tascal_auth.resources.login import Login
from tascal_auth.resources.user import UserResource 
from tascal_auth.resources.logout import Logout
from tascal_auth.resources.refresh_access_token import AccessTokenRefreshResource

with app.app_context():
    db.create_all()
    print("dbChecked.")

api.add_resource(AuthenticationResource,'/authentication')
api.add_resource(Login,'/login')
api.add_resource(UserResource,'/user')
api.add_resource(Logout,'/logout')
api.add_resource(AccessTokenRefreshResource,'/token/refresh')

