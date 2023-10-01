from db import db

class Item_TagsModel(db.Model):
    __tablename__ = "item_tags"

    regular_id=db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey("item.item_id"))
    tag_id= db.Column(db.Integer, db.ForeignKey("tag.tag_id"))
