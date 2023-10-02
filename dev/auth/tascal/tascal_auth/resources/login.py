from tascal_auth.models import UserSchema
from tascal_auth.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,get_jti,jwt_required,get_jwt,jsonify
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login_info',required=True)
    parser.add_argument('password',required=True)
    parser.add_argument('authUpdateRequest',type=str,required=False)
    @jwt_required(optional=True,refresh=True)
    def post(self):
        data = Login.parser.parse_args()
        login_info = data['login_info']
        password = data['password']
        auth = None
        oldToken = get_jwt()
        if oldToken:
            print("Request has oldToken!")
            print(oldToken)
            token = RefreshToken.find_by_refresh_token(oldToken.get("jti"))
            if token:
                token.is_invalidated = True
                token.save_to_db()
        else:
            pass

        if '@' in login_info:
            auth = Authentication.find_by_email(login_info)
        else:
            user = User.find_by_username(login_info)
            if user:
                auth = user.auth
        
        if auth and auth.check_password(password):
            uuid = auth.uuid_str()
            access_token = None
            if data['authUpdateRequest']:
                access_token = create_access_token(identity=uuid,additional_claims={"credentialUpdatePermission":"True"})
            else:
                access_token = create_access_token(identity=uuid)
            refresh_token = create_refresh_token(identity=uuid)

            save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
            save_refresh_token.save_to_db()

            user_schema = UserSchema()

            response = jsonify(message="Logged in successfully.",user=user_schema.dump(user))
            response.headers['Authorization'] = 'Bearer {}'.format(access_token)

            set_refresh_cookies(response, refresh_token)

            return response
        else:
            return jsonify(message="Loggining info is wrong!")