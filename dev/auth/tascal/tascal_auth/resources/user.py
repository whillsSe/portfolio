from marshmallow import ValidationError
from tascal_auth.models import RefreshToken, UserSchema
from tascal_auth.resources import db,Resource,reqparse,Authentication,User,set_refresh_cookies,jwt_required,get_jti,get_jwt_identity,jsonify,get_jwt,create_access_token,create_refresh_token

class UserResource(Resource):
    parser = reqparse.RequestParser()
    def get(self):
        UserResource.parser.add_argument('username',type=str,location='args')
        data = UserResource.parser.parse_args()
        target_id = data['username']
        user = User.find_by_user_id(target_id)
        if user:
            user_schema = UserSchema()
            return jsonify(message="Target user is found!",user=user_schema.dump(user).data)

    @jwt_required()
    def put(self):
        UserResource.parser.add_argument('username',type=str,required=True)
        UserResource.parser.add_argument('profilename',type=str,required=True)
        token = get_jwt()
        data = UserResource.parser.parse_args()
        current_user = get_jwt_identity()
        print(data)
        print(current_user)
        user = User.find_by_user_id(current_user)

        if not token['credentialUpdatePermission']:
            return {"message":"Invalid Access!"},400

        if not user:
            return {"message":"Account is not found."},400

        if User.find_by_username(data['username']) and user.username != data['username']:
            return {"message":"The username you entered is already used!"},400

        user_schema = UserSchema()
        try:
            updated_user = user_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages),400

        user.username = updated_user.get('username',user.username)
        user.profilename = updated_user.get('profilename',user.profilename)
        db.session.add(user)

        uuid = current_user
        access_token = create_access_token(identity=uuid)
        refresh_token = create_refresh_token(identity=uuid)

        RefreshToken.disable_tokens_by_user(uuid)

        save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
        db.session.add(save_refresh_token)

        db.session.commit()

        response = jsonify(message="User-Info updated successfully!",user=UserSchema().dump(user))
        response.headers['Authorization'] = 'Bearer {}'.format(access_token)

        set_refresh_cookies(response, refresh_token)

        return response