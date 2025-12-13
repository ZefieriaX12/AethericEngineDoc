from database.SqliteDb import db
from model.Raw_Data import Raw_Data
from model.Binary_Data import Binary_Data
from model.Data_Rel import Data_Rel
from model.Ascii_Data import Ascii_Data
from datetime import datetime
from connector.SocketMsg import SocketMsg

def storeRawSocketMsg(data: bytes, dt:datetime):
    response = Raw_Data.create(
        message = data,
        timestamptz = dt
    )
    return response.id

def storeBinaryMessage(payload:bytes, payloadSize:int):
    response = Binary_Data.create(
        payload = payload,
        payload_size = payloadSize
    )
    return response.id

def storeAsciiMessage(payload:str):
    response = Ascii_Data.create(
        payload = payload
    )
    return response.id

def storeRelationship(rawId:int, payloadId:int, dType:str):
    Data_Rel.create(
        raw_data_id = rawId,
        rel_id = payloadId,
        data_type = dType
    )
    
