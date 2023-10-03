from flask import request
from marshmallow import ValidationError
from flask_restful import inputs
from tascal_api.resources import db,Tag,Resource,DateFilterSchema,reqparse,jwt_required,get_jwt,get_jwt_identity,jsonify,TaskSchema,Task

class TaskItemResource(Resource):
    @jwt_required()
    def get(self,id):
        current_user = get_jwt_identity()
        task = Task.query.get_or_404(id)

        if task and task.author == current_user:
            task_schema = TaskSchema()
            return task_schema.dump(task)

    @jwt_required()
    def put(self,id):
        current_user = get_jwt_identity()
        data = request.get_json()
        tag_names = data.pop('tags',[])
        task_schema = TaskSchema()

        try:
            loaded_data = task_schema.load(data)
            loaded_data['author'] = current_user
        except ValidationError as err:
            print('ValidationErr')
            return {"messages":err.messages},400

        task = Task.query.get_or_404(id)

        if task.author != current_user:
            return{'message':'You cannot edit the task'},400

        current_type = task.type
        new_type = loaded_data['type']

        if current_type == 0 and new_type != 0:
            return {'message': 'Type 0 cannot be changed to another type'}, 400
        elif current_type in [1, 2] and new_type not in [1, 2]:
            return {'message': 'Type can only be changed between 1 and 2'}, 400

        # Update task with loaded_data
        for key, value in loaded_data.items():
            if hasattr(task, key):
                setattr(task, key, value)

        task.tags = []
        for tag_name in tag_names:
            tag = Tag.get_or_create(tag_name)
            task.tags.append(tag)

        db.session.commit()
        return task_schema.dump(task)
    
    @jwt_required()
    def delete(self,id):
        current_user = get_jwt_identity()
        task = Task.query.get_or_404(id)
        if task.author != current_user:
            return {"message":"Only an author can delete task"},400
        
        db.session.delete(task)
        db.session.commit()
        return {"message":"task is completely removed!"},200
