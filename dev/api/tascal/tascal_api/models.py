import enum
from flask_marshmallow import Schema

from sqlalchemy import Date, DateTime, Time, and_, or_
from tascal_api.types import EnumType
from tascal_api import db,ma
from sqlalchemy_utils import UUIDType
from marshmallow import fields,validate
import uuid

Type = enum.Enum("Type","SCHEDULE TEMPORARY PERSISTENT")

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType(binary=False), db.ForeignKey('authentication.id'), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    profilename = db.Column(db.String(255), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def find_by_username(cls,requsername):
        return cls.query.filter_by(username=requsername).first()

    @classmethod
    def find_by_user_id(cls,id):
        return cls.query.filter_by(id=id).first()

    def uuid_str(self):
        return self.id.hex

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

task_tag = db.Table(
    'task_tag',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),nullable=False),
    db.Column('task_id',UUIDType(binary=False),db.ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False),
    db.UniqueConstraint('tag_id','task_id'))

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(UUIDType(binary=False), primary_key=True,default=uuid.uuid4)
    author = db.Column(db.String(255),nullable=False)
    title = db.Column(db.String(64),default='(無題)')
    type = db.Column(db.SmallInteger) #自作のtype型をテスト運用
    rrule_string = db.Column(db.String(255),default='')
    start_date = db.Column(Date,default='1980-01-01')
    end_date = db.Column(Date,default='9999-12-31')
    start_time = db.Column(Time,nullable=True)
    due_time = db.Column(Time,nullable=True)
    completed_at = db.Column(DateTime,default=db.func.current_timestamp())
    remaining = db.Column(db.Integer,default=1)
    created_at = db.Column(db.DateTime,default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tags = db.relationship('Tag',secondary=task_tag,back_populates='tasks')

    @classmethod
    def find_by_uuid(cls,uuid):
        return cls.query.filter_by(id=uuid).first()
    
    @classmethod
    def get_tasks(cls,user_id,st_date,end_date):
        tasks = cls.query.filter(and_(cls.author==user_id,cls.start_date <= st_date,or_(cls.type==2,and_(or_(cls.type==0,cls.type==1),cls.end_date >= end_date)))).all()
        return tasks

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    tag = db.Column(db.String(64),unique=True)
    created_at = db.Column(db.DateTime,default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tasks = db.relationship('Task',secondary=task_tag,back_populates='tags')

    @classmethod
    def get_or_create(cls,tag_name):
        tag = cls.query.filter_by(tag=tag_name).first()

        if not tag:
            tag = cls(tag=tag_name)
            db.session.add(tag)
        return tag

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('id','created_at','updated_at')
        


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        exclude = ('created_at','updated_at')

    tag = fields.Str(required=True,validate=validate.And(validate.Regexp(r'^[^<>{}"/\[\];:=+*!@#$%^&*(),.?`~]*$'),validate.Length(max=100)))

class TaskSchema(ma.SQLAlchemyAutoSchema):

    title = fields.Str(required=True,validate=validate.And(validate.Regexp(r'^[^<>{}"/\[\];=+*!#$%^&*,.`]*$'),validate.Length(max=100)))
    author = fields.Str()
    type = fields.Integer()
    tags = ma.Nested(TagSchema,many=True)
    start_date = fields.Date()
    end_date = fields.Date()
    start_time = fields.Time()
    due_time = fields.Time()

    class Meta:
        model = Task
        exclude = ('created_at','updated_at')
        exclude_none = True

class DateFilterSchema(Schema):
    since = fields.Date(required=False,missing=None)
    until = fields.Date(required=False,missing=None)