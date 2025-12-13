from database.SqliteDb import db
from model.Data_Rel import Data_Rel
from model.Ascii_Data import Ascii_Data
from model.Binary_Data import Binary_Data
from model.Raw_Data import Raw_Data
from datetime import datetime

def initDB(dropTables=False):
    db.connect()
    initTables(dropTables)

def initTables(dropTables:bool):

    if Raw_Data.table_exists() == False:
        Raw_Data.create_table()
    elif dropTables & Raw_Data.table_exists():
        Raw_Data.drop_table()
        Raw_Data.create_table()
    else:
        Raw_Data.create_table()

    if Binary_Data.table_exists() == False:
        Binary_Data.create_table()
    elif dropTables & Binary_Data.table_exists():
        Binary_Data.drop_table()
        Binary_Data.create_table()
    else:
        Binary_Data.create_table()

    if Ascii_Data.table_exists() == False:
        Ascii_Data.create_table()
    elif dropTables & Ascii_Data.table_exists():
        Ascii_Data.drop_table()
        Ascii_Data.create_table()
    else:
        Ascii_Data.create_table()

    if Data_Rel.table_exists() == False:
        Data_Rel.create_table()
    elif dropTables & Data_Rel.table_exists():
        Data_Rel.drop_table()
        Data_Rel.create_table()
    else:
        Data_Rel.create_table()