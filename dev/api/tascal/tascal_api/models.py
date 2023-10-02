import enum

from sqlalchemy import Date, DateTime, Time
from api.tascal.tascal_api.types import EnumType
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
    tuple(db.UniqueConstraint('tag_id','task_id')),
    db.Column(db.Integer,primary_key=True),
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),nullable=False),
    db.Column('task_id',UUIDType(binary=False),db.ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False))

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(UUIDType(binary=False), primary_key=True,default=uuid.uuid4)
    author = db.Column(db.String(255),nullable=False)
    title = db.Column(db.String(64),default='(無題)')
    type = db.Column(EnumType(enum_class=Type)) #自作のtype型をテスト運用
    rrule_string = db.Column(db.String(255),default='')
    start_date = db.Column(Date,default='1980-01-01')
    end_date = db.Column(Date,default='9999-12-31')
    start_time = db.Column(Time,nullable=True)
    end_time = db.Column(Time,nullabe=True)
    completed_at = db.Column(DateTime,default=db.func.current_timestamp())
    remaining = db.Column(db.Integer,default=1)
    created_at = db.Column(db.DateTime,default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tags = db.relationship('Tag',secondary=task_tag,back_populates='tasks')

    @classmethod
    def find_by_uuid(cls,uuid):
        return cls.query.filter_by(id=uuid).first()

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(unsigned=True),primary_key=True,autoincrement=True)
    tag = db.Column(db.String(64),unique=True)
    created_at = db.Column(db.DateTime,default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tasks = db.relationship('Task',secondary=task_tag,back_populates='tags')

class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        exclude = ('created_at','updated_at')

    tag = fields.Str(required=True,validate=validate.And(validate.Regexp(r'^[^<>{}"/\[\];:=+*!@#$%^&*(),.?`~]*$'),validate.Length(max=100)))

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

    title = fields.Str(required=True,validate=validate.And(validate.Regexp(r'^[^<>{}"/\[\];=+*!#$%^&*,.`]*$'),validate.Length(max=100)))
    task = fields.Str(required=True,validate=validate.And(validate.Regexp(r'^[^<>{}"/\[\]=+*!@#$%^&*().?`~]*$'),validate.Length(max=100)))
    tags = ma.Nested(TagSchema,many=True)