from tascal_api import db,bcrypt,jsonify,SQLAlchemyError
from tascal_api.models import Tasks,TaskSchema
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity