
from flask import request
from marshmallow import ValidationError
from flask_restful import inputs
from tascal_api.resources import db,Tag,Resource,DateFilterSchema,reqparse,jwt_required,get_jwt,get_jwt_identity,jsonify,TaskSchema,Task

class TaskResource(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        loaded_dates = DateFilterSchema().load(data)
        tasks = Task.get_tasks(current_user,loaded_dates['since'],loaded_dates['until'])

        task_schema = TaskSchema(many=True)
        result = task_schema.dump(tasks)

        return result

    @jwt_required()
    def post(self):
        
        current_user = get_jwt_identity()
        data = request.get_json()
        tag_names = data.pop('tags',[])
        task_schema = TaskSchema()

        print(data['start_date'])

        try:
            loaded_data = task_schema.load(data)
            loaded_data['author'] = current_user
        except ValidationError as err:
            print('ValidationErr')
            return {"messages":err.messages},400
        
        try:
            task = Task(**loaded_data)
            db.session.add(task)
            db.session.flush()

            for tag_name in tag_names:
                tag = Tag.get_or_create(tag_name)
                task.tags.append(tag)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        
        return jsonify(task_schema.dump(task))
            

        
        
