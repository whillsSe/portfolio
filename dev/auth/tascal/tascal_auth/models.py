import random
import string
from tascal_auth import db,ma,bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy_utils import UUIDType
from marshmallow import fields,validate
import uuid

class Authentication(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(UUIDType(binary=False), primary_key=True,default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User',back_populates='auth',uselist=False)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_uuid(cls,id):
        return cls.query.filter_by(id=id).first()

    def uuid_str(self):
        return self.id.hex

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self,email,password):
        self.email = email
        self.password = self.hash_password(password)

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    refresh_token = db.Column(db.String(255), primary_key=True)
    user = db.Column(UUIDType(binary=False), nullable=False)
    is_invalidated = db.Column(db.Boolean, nullable=False,default=False)
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

    @classmethod
    def is_refresh_token_valid(cls,token):
        record = cls.find_by_refresh_token(token)
        if (not record) or record.is_invalidated == False:
            return False
        return True

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
    username = db.Column(db.String(255), nullable=False, unique=True)
    profilename = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    auth = db.relationship('Authentication',back_populates='user',uselist=False)

    @classmethod
    def find_by_username(cls,requsername):
        return cls.query.filter_by(username=requsername).first()
    
    @classmethod
    def find_by_user_id(cls,id):
        return cls.query.filter_by(id=id).first()
    
    def uuid_str(self):
        return self.id.hex
    
    def __init__(self,user_id,username):
        self.id = user_id
        self.username = username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def generate_random_username(length=10):
        if length < 5 or length > 15:
            raise ValueError("Username length must be between 5 and 15 characters")
        while True:
            prefix_length = random.randint(1, length - 4)  # Ensure there's room for at least 4 random alphanumeric characters
            prefix = ''.join(random.choices(string.ascii_letters, k=prefix_length))
            suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length - prefix_length))
            username:string = prefix + suffix
            if not User.find_by_username(username):
                return username

class AuthenticationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Authentication
        exclude = ('created_at','updated_at')
    email = fields.Email(required=True,validate=fields.validate.Length(min=1,max=120))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('created_at','updated_at')
    username = fields.Str(required=True,validate=validate.Regexp(r'^[a-zA-Z][a-zA-Z0-9]{4,14}$'))
    profilename = fields.Str(required=True,validate=validate.Regexp(r'^[^<>{}"/\[\];:=+*!@#$%^&*(),.?`~]*$'))