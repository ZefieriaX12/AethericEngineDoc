from peewee import SqliteDatabase

from pathlib import Path



current_dir = Path(__file__).resolve().parent.parent

db_path = f"{current_dir}//storage.db"

db = SqliteDatabase(db_path)

