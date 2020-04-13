from typing import Dict, List, Union
from db import db

# all keys in this dict are strings
ItemJson = Dict[str, Union[int, float, str]]


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")
    # Self is the objecct we call the method with
    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJson:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    # return has to be in quotes because item model dosn't exist
    # python will look to return the current class after the item value
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
