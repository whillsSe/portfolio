from tascal_auth.models import UserSchema
from tascal_auth.resources import Resource,reqparse,Authentication,User,jwt_required,get_jwt_identity,jsonify

class UserResource(Resource):
    parser = reqparse.RequestParser()
    def get(self):
        UserResource.parser.add_argument('username',type=str,location='args')
        data = UserResource.parser.parse_args()
        target_id = data['username']
        user = User.find_by_user_id(target_id)
        user_schema = UserSchema()
        return jsonify(message="Target user is found!",user=user_schema.dump(user).data)

    @jwt_required()
    def post(self):
        UserResource.parser.add_argument('username',type=str,required=True)
        UserResource.parser.add_argument('profilename',type=str,required=True)
        current_user = get_jwt_identity()
        data = UserResource.parser.parse_args()
        print(data)
        if not Authentication.find_by_uuid(current_user):
            return {'message':"Something wrong in registering your account."},400
        
        if User.find_by_username(data['username']):
            return {"message":"The username you entered is already registered!"},400
        
        user = Authentication.find_by_uuid(current_user).user
        user.username = data['username']
        user.profilename = data['profilename']
        user.save_to_db()
        return jsonify(message="User-Info registered successfully!",user=UserSchema().dump(user))

    @jwt_required()
    def put(self):
        UserResource.parser.add_argument('username',type=str,required=True)
        UserResource.parser.add_argument('profile',type=str,required=True)
        current_user = get_jwt_identity()
        data = UserResource.parser.parse_args()
        auth = Authentication.find_by_uuid(current_user)

        if not auth:
            return {"message":""},400
        
        if User.find_by_username(data['username']) and auth.user.id != data['username']:
            return {"message":"Id you entered is already registered!"},400
        
        user = Authentication.find_by_uuid(current_user).user
        user.user_id = data['username']
        user.username = data['profilename']
        user.save_to_db()

        return jsonify(message="User-Info updated successfully!")