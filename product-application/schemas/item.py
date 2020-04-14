from ma import ma
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.ModelSchema):
    class Meta:
        meta = ItemModel
        load_only = ('store',)
        dump_only = ('id',)
        include_fk = True #to conscider foreign keys
