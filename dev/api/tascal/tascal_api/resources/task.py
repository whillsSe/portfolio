
import datetime
from marshmallow import ValidationError

from sqlalchemy import DATE, TIME
from tascal_api.resources import db,Resource,reqparse,jwt_required,get_jwt,get_jwt_identity,jsonify,TaskSchema,Task

class TaskResource(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def post(self):
        TaskResource.parser.add_argument('title',type=str)
        TaskResource.parser.add_argument('type',type=str,require=True)
        TaskResource.parser.add_argument('rrule_string',type=str)
        TaskResource.parser.add_argument('start_date',type=DATE)
        TaskResource.parser.add_argument('end_date',type=DATE)
        TaskResource.parser.add_argument('start_time',type=TIME)
        TaskResource.parser.add_argument('due_time',type=TIME)
        TaskResource.parser.add_argument('tags',type=str)

        current_user = get_jwt_identity()
        data = TaskResource.parser.parse_args()

        task_schema = TaskSchema()

        tags = data['tags'].splice(",")
        try:
            task_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages),400
        
        task = Task(**task_schema)
        db.session.add(task)
        db.session.flush()

        
        
