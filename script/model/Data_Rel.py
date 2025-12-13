from peewee import Model, IntegerField, BlobField, TextField, BooleanField
from model.BaseModel import BaseModel

class Data_Rel(BaseModel):
    raw_data_id = IntegerField()
    rel_id = IntegerField()
    data_type = TextField()

