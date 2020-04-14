from db import db
from typing import Dict, Union

UserJson = Dict[str, Union[int, str]]


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable= False,unique=True)
    password = db.Column(db.String(80), nullable= False)

    # Using the nullable as false makes allows us to remove 
    # __init__ since we are using nullable
    #def __init__(self, username: str, password: str):
    #    self.username = username
    #    self.password = password

    # Return a dictionary here
    def json(self) -> UserJson:
        return {"id": self.id, "username": self.username}

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
