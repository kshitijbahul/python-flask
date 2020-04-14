from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many = True)# to define FK relationship
    class Meta:
        meta = StoreModel
        dump_only = ('id',)
        include_fk = True
