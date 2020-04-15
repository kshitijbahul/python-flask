from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from marshmallow import ValidationError
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

BLANK_ERROR= "'{}' field cannot be left blank!"
USERNAME_ALREADY_EXISTS = "A user with that username already exists."
USER_CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGIN_SUCCESSFUL = "User <id={}> successfully logged out."
USER_NOT_CONFIRMED = "'{}' You have not confirmed registeration. Check your email"
USER_ALREADY_ACTIVE = "'{} is already active"
USER_IS_NOW_ACTIVATED = "'{}' has been activated successfully"
user_schema = UserSchema()



class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())#

        if UserModel.find_by_username(user.username):
            return {"message": USERNAME_ALREADY_EXISTS}, 400

        #user = UserModel(**user_data) # not needed since model is created by marshmallo
        user.save_to_db()

        return {"message": USER_CREATED_SUCCESSFULLY}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message":USER_NOT_FOUND }, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data.username)

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, user_data.password):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            if user.activated: 
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return USER_NOT_CONFIRMED.format(user.username), 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGIN_SUCCESSFUL.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class UserConfirmation(Resource):
    @classmethod
    def get(cls,userid: int):
        #find the user by id 
        user = UserModel.find_by_id(userid)
        if (user and user.activated == False): 
             # activate it
            #save to db
            #return message
            user.activated = True
            user.save_to_db()
            return {"message":USER_IS_NOW_ACTIVATED.format(user.username)},200
        elif user.activate:
            return {"message":USER_ALREADY_ACTIVE.format(userid)}, 200
        return {"message":USER_NOT_FOUND}, 400

       
