from peewee import Model, IntegerField, BlobField, TextField, BooleanField, AutoField
from model.BaseModel import BaseModel

class Binary_Data(BaseModel):
    id = AutoField()
    payload = BlobField()
    payload_size = IntegerField()

    class Meta:
        table_name = "msgbinary"