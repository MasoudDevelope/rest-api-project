import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema,StoreUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import StoreModel

blp=Blueprint("Stores","stores",description = "Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return{"message":"store deleted!"}


    @blp.arguments(StoreUpdateSchema)
    @blp.response(200,StoreSchema)
    def put(self,store_data,store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating the store was not implemented!")



@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
     #   return f"stores: {list(stores.values())}"
     return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(cls,store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="a store with that name already exists!")
        except SQLAlchemyError:
            abort(500,message="an error occured while creating the store!")
        return store

 