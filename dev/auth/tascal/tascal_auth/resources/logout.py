from tascal_auth.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,get_jti,jwt_required,get_jwt,jsonify
class Logout(Resource):
    parser = reqparse.RequestParser()
    @jwt_required(refresh=True)
    def get(self):
        tokenString = get_jwt().get("jti")
        token = RefreshToken.find_by_refresh_token(tokenString)
        token.is_invalidated = True

        token.save_to_db()
        
        return {"message":"Logged out successfully!"}