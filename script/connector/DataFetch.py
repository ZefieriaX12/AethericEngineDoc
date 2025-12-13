# AI was used to figure out that I should use Socket instead of WebSockets...

import socket
import parser.DataParser as dParser

from datetime import timezone, timedelta, datetime
from connector.SocketMsg import SocketMsg
from connector.SConnector import SConnector

import logging
logger = logging.getLogger(__name__)

def fetchStoreData(host:str, port:int, jwt:str, msgCount:int):

    with socket.create_connection((host,port), timeout=2) as sock:
        logger.info(f"Successfully connected to {host}:{port}")
        
        connector = SConnector(sock, jwt)

        connector.startReceiving()
        
        logger.info("Start fetching messages")
        
        dParser.processMessage(connector, msgCount)
        
        logger.info(f"Saved {msgCount} messages")
             
        connector.stopReceiving()
        connector.drainMessages()
           
