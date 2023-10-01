from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, StoreModel , ItemModel
from schemas import TagSchema , TagAndItemSchema

blp=Blueprint("Tag","tag",description="operation on tags")

@blp.route("/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tag.all()

    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def post(self,tag_data,store_id):
        tag=TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        try:
            tag=TagModel.query.get_or_404(tag_id)
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)

        if not tag.item :
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag deleted!"}
        abort(400,message="couldn not delete the tag. make sure it's not linked to any items")
           
    
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkItemTag(MethodView):
    @blp.response(200,TagAndItemSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        item.tag.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return {"message":f"item and tag got linked! tag={tag} & item = {item}"}
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        item.tag.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return {"message":f"item and tag got unlinked! tag={tag} & item = {item}"}
    








