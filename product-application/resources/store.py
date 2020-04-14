from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from models.store import StoreModel
from schemas.store import StoreSchema



ITEM_NOT_FOUND = "'{}' not found."
STORE_ALREADY_EXISTS = "A store with name '{}' already exists."
STORE_CREATION_ERROR = "An error occurred while creating the store."
STORE_DELETED = "Store deleted."
store_schema= StoreSchema()
store_list_schema = StoreSchema(many = True)

class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"message": ITEM_NOT_FOUND.format("Store")}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return (
                {"message": STORE_ALREADY_EXISTS.format(name)},
                400,
            )

        store = StoreModel(name=name)#because its a model subclass
        try:
            store.save_to_db()
        except:
            return {"message": STORE_CREATION_ERROR}, 500

        return store_schema.dump(store), 201
    
    @classmethod
    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    def get(self):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}