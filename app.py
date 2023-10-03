import requests
from flask import Flask,jsonify
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
from db import db
import models
from dotenv import load_dotenv
#comment
import os
from flask_jwt_extended import JWTManager
import secrets
from flask_migrate import Migrate






def create_app(db_url=None):
    load_dotenv()
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)
    migrate=Migrate(app,db)
    api=Api(app)

    #app.config["JWT_SECRET_KEY"]=secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"]="181186031699974865317766408573432751934"
    jwt=JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify({
                "description":"the user has logged out!"
            }),401
        )
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {
                    "description":"the token is not fresh",
                    "error":"fresh token required"
                }
            )
        )

    @jwt.additional_claims_loader
    def additional_claim_callback(identity):
        if identity == 1:
            return {"isAdmin":True}
        else:
            return {"isAdmin":False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {
                    "message":"The token has expired.","error":"Token Expired!"
                },401
            )
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify(
                {"message":"Signiture Verification Failed!","error":"invalid token!"
                 
                 },401
            )
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {"message":"Request does not contain an access token.",
                 "error":"authorization required"}
                ,401
            )
        )
    #with app.app_context():
       # db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app

"""        @app.get("/store")
        def get_stores():
            return f"stores: {list(stores.values())}"


        @app.post("/store")
        def create_store():
            store_data = request.get_json()
            if ("name" not in store_data):
                abort(400,message="ensure you enter store name!")
            for store in stores.values():
                if store["name"]==store_data["name"] :
                    abort(400,message="store already exists!")
            store_id=uuid.uuid4().hex
            store = {"store_id":store_id,**store_data}  
            stores[store_id]=store
            return{"message":f" new store was added : {store}"},201
            
        @app.post("/item")
        def create_item():
            item_data = request.get_json()
            if (
                "price" not in item_data or
                "name" not in item_data or
                "store_id" not in item_data
            ):
                abort(400,message="make sure your enter store_id, price, and name of the item!")
            for item in items.values():
                if (
                    item_data["name"]==item["name"] and
                    item_data["store_id"]==item["store_id"]
                ):
                    abort(400,message="item already in the store!")
            if item_data["store_id"] not in stores:
                abort(404,message="store not found!") 
            item_id = uuid.uuid4().hex
            item = {"item_id":item_id,**item_data}
            items[item_id]=item
            return item,201


        @app.get("/items")
        def get_items():
            return f"items: {list(items.values())}",201

        @app.get("/store/<string:store_id>")
        def get_store(store_id):
            try:
                return{"message":stores[store_id]}
            except KeyError:
                abort(404,message="store id does not match any sotre id in the database!") 
        @app.get("/item/<string:item_id>")
        def get_item(item_id):
            try:
                return({"message":items[item_id]},201) 
            except KeyError:
                abort(404,message="item not found!")

        @app.delete("/item/<string:item_id>")
        def delete_item(item_id):
            try:
                del items[item_id]
                return {"message":"item deleted!"}
            except KeyError:
                abort(404,message="item not found!")

        @app.put("/item/<string:item_id>")
        def update_item(item_id):
            item_data = request.get_json()
            if ("name" not in item_data
                or "price" not in item_data):
                abort(400,message="make sure you enter name and price")
            try:
                item=items[item_id]
                item |= item_data
                return item
            except KeyError:
                abort(404,message="item not found!")

        @app.delete("/store/<string:store_id>")
        def delete_store(store_id):
            if store_id not in stores:
                abort(400,"store not found!")
            del stores[store_id]
            return {"message":"store deleted!"}
        @app.put("/store/<string:store_id>")
        def update_store(store_id):
            store_data = request.get_json()
            if "name" not in store_data:
                abort(404,message="make sure enter store's name")
            try:
                store = stores[store_id]
                store |= store_data
                return store
            except KeyError:
                abort(400,message="store not found!")    
"""