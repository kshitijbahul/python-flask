from ma import ma
from models.user import UserModel

class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",) # telling to use this field only for loading and not returing 
        dump_only = ("id","activated",) # telling to use this field only for returing and not accepting
    