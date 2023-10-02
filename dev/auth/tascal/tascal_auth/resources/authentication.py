from flask_jwt_extended import create_access_token, create_refresh_token,get_jti,set_refresh_cookies,get_jwt,get_jwt_identity,jwt_required
from flask_restful import Resource,reqparse
from tascal_auth.resources import db,Authentication,RefreshToken,User,bcrypt,jsonify,SQLAlchemyError

class AuthenticationResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',type=str,required=True,help="This field cannnot be blank.")
    parser.add_argument('password',type=str,required=True,help="This field cannnot be blank.")

    def post(self):
            data = AuthenticationResource.parser.parse_args()
            if Authentication.find_by_email(data['email']):
                return {"message":"A user using the email you entered already exists"},400

            auth = Authentication(data["email"],data["password"])
            try:
                db.session.add(auth)
                db.session.flush()

                uuid = auth.uuid_str() #改めてdbに読み込みに行ってくれるのか、変数内に確保されてるものが返されるのか知りたい
                print(uuid)
                username = User.generate_random_username()

                user = User(uuid,username)
                db.session.add(user)

                access_token = create_access_token(identity=uuid,additional_claims={"credentialUpdatePermission":"True"})
                refresh_token = create_refresh_token(identity=uuid)

                save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
                db.session.add(save_refresh_token)

                db.session.commit()

                response = jsonify(message="User created successfully.")
                response.headers['Authorization'] = 'Bearer {}'.format(access_token)

                set_refresh_cookies(response, refresh_token)

                return response

            except SQLAlchemyError as e:
                db.session.rollback()
                return {"message": "An error occurred while creating the user: {}".format(str(e))}, 500

    @jwt_required(refresh=False)
    def put(self):
        data = AuthenticationResource.parser.parse_args()
        token = get_jwt()
        print(token)
        try:
            auth = Authentication.find_by_uuid(get_jwt_identity())
            if not token['credentialUpdatePermission']:
                return {"message":"Invalid Access!"},400

            if Authentication.find_by_email(data['email']) and auth.email != data['email']:
                return {"message":"A user with that email already exists"},400

            auth.email = data["email"]
            auth.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            db.session.add(auth)

            uuid = auth.uuid_str()
            access_token = create_access_token(identity=uuid)
            refresh_token = create_refresh_token(identity=uuid)

            RefreshToken.disable_tokens_by_user(uuid)

            save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
            db.session.add(save_refresh_token)

            db.session.commit()

            response = jsonify(message="Authentication Info is updated successfully.")
            response.headers['Authorization'] = 'Bearer {}'.format(access_token)

            set_refresh_cookies(response, refresh_token)

            return response
        
        except SQLAlchemyError as e:
                db.session.rollback()
                return {"message": "An error occurred while editing the authentication: {}".format(str(e))}, 500