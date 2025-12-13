from connector.SocketMsg import SocketMsg
from datetime import timezone, timedelta, datetime

import socket
import database.DataWriter as writer

import logging
logger = logging.getLogger(__name__)

class SConnector():
    sockConn = None
    jwt = None

    tz_offset = +8.0
    tzinfo = timezone(timedelta(hours=tz_offset))
    socketReadBufferSize = 1048576

    def __init__(self, sockConn:socket, jwt:str):
        self.sockConn = sockConn
        self.jwt = jwt

    def startReceiving(self):
        logger.info("Sending start message")
        request = f"AUTH {self.jwt}"
        self.sockConn.send(request.encode())
        logger.info("Start message sent")

    def stopReceiving(self):
        logger.info(f"Sending termination message")
        request = "STATUS"
        self.sockConn.send(request.encode())
        logger.info("Termination message sent")

    def drainMessages(self):
        logger.info("Draining remaining messages in pipe line")
        i = 0
        messagesAfterClose = []
        while True:
            try:
                response = self.sockConn.recv(1048576)
                messagesAfterClose.append(SocketMsg(i, response, datetime.now(self.tzinfo)))
                i = i + 1
            except TimeoutError as err:
                logger.info(f"No more response from Socket")
                break 

    def fetchNext(self) -> SocketMsg:
        response = self.sockConn.recv(self.socketReadBufferSize)
        
        currentTime = datetime.now(self.tzinfo)
        msgIndex = writer.storeRawSocketMsg(response, currentTime)

        msg = SocketMsg(msgIndex, response, currentTime)
            
        return msg
