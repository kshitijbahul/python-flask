from db import db
from requests import Response,post
from typing import Dict, Union
from flask import request,url_for
from libs.mailgun import Mailgun


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable= False,unique=True)
    password = db.Column(db.String(80), nullable= False)
    email = db.Column(db.String(80), nullable =False, unique= True)
    activated = db.Column(db.Boolean, default= False)

    # Using the nullable as false makes allows us to remove 
    # __init__ since we are using nullable
    #def __init__(self, username: str, password: str):
    #    self.username = username
    #    self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email : str) -> "UserModel":
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
    
    def sendConfirmationEmail(self) -> Response:
        #talk to mailgun
        #respond
        #upto not including the last info, name of the resource for user confirm
        link = request.url_root[0:-1]+ url_for('userconfirmation',userid=self.id)
        email = [self.email, "dev@aogonline.tech"]
        subject = "Registeration Confirmation"
        text = "Please clisck the link to confirm your registeration {link}"
        html = '<html>Please clisck the link to confirm your registeration <a href="{link}"</a></html>'
        return Mailgun.send_email(email,subject,text,html)


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
