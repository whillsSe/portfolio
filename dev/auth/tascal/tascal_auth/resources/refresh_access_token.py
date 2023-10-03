from tascal_auth.models import UserSchema
from tascal_auth.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,get_jti,jwt_required,get_jwt,jsonify,get_jwt_identity

class AccessTokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        
        response = {"message":"token refreshed"},200
        response.headers['Authorization'] = 'Bearer {}'.format(access_token)

        return response