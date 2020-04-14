from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        load_only = ("password",) # telling to use this field only for loading and not returing 
        dump_only = ("id",) # telling to use this field only for returing and not accepting
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)