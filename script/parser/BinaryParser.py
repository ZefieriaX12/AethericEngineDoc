# AI was used to figure out how to convert 5 bytes to integer
# 
from connector.SConnector import SConnector
import parser.Utils as utils

import logging
logger = logging.getLogger(__name__)

class BinaryParserResponse:
    payloadSize = int

    incomplete: bool
    badFetch: bool

    payload: bytearray
    remainingPayload: bytearray
    reference: list[int]

    def __init__(self, payloadSize, payload, remainingPayload, incomplete, badFetch, references):
        self.payloadSize = payloadSize
        self.payload = payload
        self.remainingPayload = remainingPayload
        self.incomplete = incomplete
        self.badFetch = badFetch
        self.reference = references

def fetchSize(startingBytes:bytes) -> int:
    # This was AI assisted
    return int.from_bytes(startingBytes, "little")

# Since we know the size, we can just use slice to extract the message
def binaryParsing(firstMsg:bytes, sConn: SConnector, refId:int) -> BinaryParserResponse:
    
    referenceList = []
    referenceList.append(refId)

    data = firstMsg
    payloadSize = fetchSize(data[1:6])
    bufToParse = bytearray(data[6:])
    
    inCompleteData:bool
    badDataFetch:bool

    while True:        

        if payloadSize == len(bufToParse):
            logger.debug("All Data Fetched")

            inCompleteData = False
            badDataFetch =  False

            return BinaryParserResponse(payloadSize, bufToParse, bytearray(), inCompleteData, badDataFetch, referenceList)

            # return payloadSize, bufToParse, bytearray(), True

        elif payloadSize > len(bufToParse):
            logger.debug("Incomplete Data, fetch more")
            
            nextMsg = sConn.fetchNext()
            if nextMsg.isEmpty():
                logger.debug("Data Stream Ended but Payload is incomplete")       

                inCompleteData = True
                badDataFetch =  True

                return BinaryParserResponse(payloadSize, bufToParse, bytearray(), inCompleteData, badDataFetch, referenceList)

                # return payloadSize, bufToParse, bytearray(nextMsg), False
            
            referenceList.append(nextMsg.order)

            if utils.detectType(nextMsg.data[0:1]) != "ASCII":
                bufToParse = bufToParse + bytearray(nextMsg.data)
            else:
                logger.debug("Data Stream Broken, Next Message is a different type")
                inCompleteData = True
                badDataFetch =  False
                return BinaryParserResponse(payloadSize, bufToParse, bytearray(nextMsg.data), inCompleteData, badDataFetch, referenceList)
        else:
            logger.debug("More Data Than Expected Fetched")
            inCompleteData = False
            badDataFetch =  False
            return BinaryParserResponse(payloadSize, bufToParse[0:payloadSize], bytearray(bufToParse[payloadSize:]), inCompleteData, badDataFetch, referenceList)
            # return payloadSize, bufToParse[0:payloadSize], bytearray(bufToParse[payloadSize:]), True


