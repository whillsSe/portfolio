from tascal_auth import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType

class Authentication(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(UUIDType(binary=False), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    refresh_token = db.Column(db.String(255), primary_key=True)
    user = db.Column(UUIDType(binary=False), nullable=False)
    is_invalidated = db.Column(db.String(255), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType(binary=False), db.ForeignKey('authentication.id'), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    profilename = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


# Add foreign key relationships
User.authentication = db.relationship('Authentication', back_populates='users', uselist=False)
