from peewee import Model, IntegerField, BlobField, TextField, BooleanField, AutoField
from model.BaseModel import BaseModel

class Ascii_Data(BaseModel):
    id = AutoField()
    payload = TextField()

    class Meta:
        table_name = "msgascii"

