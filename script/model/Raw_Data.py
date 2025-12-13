from peewee import Model, IntegerField, BlobField, TextField, AutoField
from model.BaseModel import BaseModel

class Raw_Data(BaseModel):
    id = AutoField()
    message = BlobField()
    timestamptz = TextField()

