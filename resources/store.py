from flask_restful import Resource
from models.store import StoreModel
ITEM_NOT_FOUND = "'{}' not found."
STORE_ALREADY_EXISTS = "A store with name '{}' already exists."
STORE_CREATION_ERROR = "An error occurred while creating the store."
STORE_DELETED = "Store deleted."

class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": ITEM_NOT_FOUND.format("Store")}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return (
                {"message": STORE_ALREADY_EXISTS.format(name)},
                400,
            )

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": STORE_CREATION_ERROR}, 500

        return store.json(), 201
    
    @classmethod
    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    def get(self):
        return {"stores": [x.json() for x in StoreModel.find_all()]}
