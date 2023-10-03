import requests 
import os

from db import db
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from models import UserModel
from schemas import UserSchema
from schemas import UserRegisterSchema
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,create_refresh_token,get_jwt_identity
from blocklist import BLOCKLIST
from sqlalchemy import or_


blp=Blueprint("User","user",description="operations on user")
domain =os.getenv("MAILGUN_DOMAIN")
api_key=os.getenv("MAILGUN_API_KEY")
def send_simple_message(to,subject,body):
    request = requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", api_key),
		data={"from": f"HR <mailgun@{domain}>",
			"to": [to],
			"subject": subject,
			"text": body})
    return request



@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self,user_data):
        if UserModel.query.filter( or_(UserModel.username==user_data["username"] ,
                                  UserModel.email==user_data["email"]) 
                                  ).first():
            abort(500,message=f"A user with the username or email already exists!")
        user = UserModel(username=user_data["username"],
                         email=user_data["email"],
                         password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()
        send_simple_message(to=user.email,
                            subject="Successfully Signed Up!",
                            body = f"Hi {user.username}. Welcome to our World!"
                            )
        return user
@blp.route("/user/<int:user_id>")
class UserList(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user
    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "user removed!"
@blp.route("/user")
class User(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
@blp.route("/login")
class USerLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.user_id,fresh=True)
            refresh_token=create_refresh_token(identity=user.user_id)
            return {"access_token":access_token,"refresh_token":refresh_token}
        abort(401,message="Invalid Credentials!")
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"message":"succesfully logged out"}
        
@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        access_token=create_access_token(identity=current_user,fresh=False)
        # it you want to only be able to use the not fresh token once you can code the next two lines
        jti=get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return({"access_token":access_token})

