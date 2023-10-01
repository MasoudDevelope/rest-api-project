from db import db

class StoreModel(db.Model):
    __tablename__ = "store"
    
    store_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    item=db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade="all,delete")
    tag=db.relationship("TagModel",back_populates="store",lazy="dynamic",cascade="all,delete")
