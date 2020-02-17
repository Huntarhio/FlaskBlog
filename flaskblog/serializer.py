from marshmallow_sqlalchemy import  ModelSchema, SQLAlchemyAutoSchema
from marshmallow import fields
from flaskblog.models import User, Post

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        relationship = True
        load_instance = True

class PostSchema(SQLAlchemyAutoSchema):
    class meta:
        model = Post
        include_fk = True
        load_instance = True

