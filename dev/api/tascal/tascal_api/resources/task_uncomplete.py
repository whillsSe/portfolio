import datetime
from flask import request
from marshmallow import ValidationError
from flask_restful import inputs
from tascal_api.resources import db,Tag,Resource,DateFilterSchema,reqparse,jwt_required,get_jwt,get_jwt_identity,jsonify,TaskSchema,Task

class TaskUncomplete(Resource):
    @jwt_required()
    def post(self,id):
        current_user = get_jwt_identity()
        task = Task.query.get_or_404(id)
        if task.author != current_user:
            return {"message":"Only an author can uncomplete task"},400
        
        if task.type == 0:
            return {"message":"Schedule cannnot be completed"},400
        
        task.remaining += 1

        db.session.add(task)
        db.session.commit()

        return TaskSchema().dump(task)