from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,set_refresh_cookies,get_jwt_identity,get_jti,get_jwt,verify_jwt_in_request
from tascal_auth.models import Authentication,User,RefreshToken
from tascal_auth import db,bcrypt,jsonify,SQLAlchemyError