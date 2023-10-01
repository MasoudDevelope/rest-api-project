from db import db

class TagModel(db.Model):
    __tablename__="tag"

    tag_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=False)
    store_id=db.Column(db.Integer,db.ForeignKey("store.store_id"))
    store=db.relationship("StoreModel",back_populates="tag")
    item=db.relationship("ItemModel",back_populates="tag",secondary="item_tags")



