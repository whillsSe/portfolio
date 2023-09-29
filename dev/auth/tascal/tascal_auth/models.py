from tascal_auth import db,ma
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy_utils import UUIDType
import uuid

class Authentication(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(UUIDType(binary=False), primary_key=True,default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User',back_populates='auth',uselist=False)

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_uuid(cls,uuid):
        return cls.query.filter_by(id=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self,email,password):
        self.email = email
        self.password = password

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    refresh_token = db.Column(db.String(255), primary_key=True)
    user = db.Column(UUIDType(binary=False), nullable=False)
    is_invalidated = db.Column(db.String(255), nullable=False,default=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def find_by_refresh_token(cls,token):
        return cls.query.filter_by(refresh_token=token).first()
    
    @classmethod
    def disable_tokens_by_user(cls,user_id):
        tokens = cls.query.filter_by(user=user_id).all()
        for token in tokens:
            token.is_invalidated = True
        db.session.commit()

    def __init__(self,refesh_token,user_id):
        self.refresh_token = refesh_token
        self.user = user_id
        self.expiration_time = datetime.utcnow() + timedelta(days=30)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType(binary=False), db.ForeignKey('authentication.id'), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True,default=uuid.uuid4)
    profilename = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    auth = db.relationship('Authentication',back_populates='user',uselist=False)

    @classmethod
    def find_by_username(cls,requsername):
        return cls.query.filter_by(username=requsername).first()
    
    def find_by_user_id(cls,uuid):
        return cls.query.filter_by(id=uuid).first()
    
    def __init__(self,user_id):
        self.id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('created_at','updated_at')