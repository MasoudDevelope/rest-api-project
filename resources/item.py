from flask_smorest import Blueprint,abort
from flask.views import MethodView
from schemas import ItemSchema,ItemUpdateSchema
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required,get_jwt

blp=Blueprint("Items","items",description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
       """ try:
            #return {"message":items[item_id]}
            return items[item_id]
        except KeyError:
            abort(404,message="item not found!")"""
       item = ItemModel.query.get_or_404(item_id)
       return item  
    @jwt_required()#fresh=True means this function needs a fresh access_token
    def delete(self,item_id):
        jwt=get_jwt()
        print(jwt.get("fresh"))
        print(jwt.get("access_token"))
        if not jwt.get("isAdmin") :
            abort(404,message="deletion failed. Admin priviledge required!")
        if jwt.get("fresh")== False :
            abort(401,message="fresh token required!")
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return{"message":"item deleted!"}

    @jwt_required()       
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get_or_404(item_id)
        item.name=item_data["name"]
        item.price=item_data["price"]

        db.session.add(item)
        db.session.commit()

    
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
        if ItemModel.query.filter(ItemModel.name==item_data["name"]).first():
            abort(500,message="item already exists!")
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an error occured while inserting the item!")
        return item,201
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
