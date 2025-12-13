from peewee import Model
from database.SqliteDb import db

class BaseModel(Model):
    class Meta:
        database = db