from tascal_auth.models import UserSchema
from tascal_auth.resources import request,Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,get_jti,jwt_required,get_jwt,jsonify,get_jwt_identity

class AccessTokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        refreshToken = get_jwt()
        print(refreshToken)
        current_user = get_jwt_identity()
        if RefreshToken.is_refresh_token_valid(refreshToken["jti"]):
            access_token = create_access_token(identity=current_user)
            
            response = jsonify(message="token refreshed")
            response.headers['Authorization'] = 'Bearer {}'.format(access_token)
        else:
            response = {"message":"Invalidated token!"},400

        return response