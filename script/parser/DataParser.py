from connector.SConnector import SConnector
import parser.Utils as utils
import parser.BinaryParser as binaryParser
import parser.AsciiParser as asciiParser

import database.DataWriter as dataWriter



import logging
logger = logging.getLogger(__name__)


def processMessage(sConnector:SConnector, msgCount) -> str:
    endLoop = False
    dataToParse = None

    remainingBuf = bytearray()
    savedMsgCount = 0
    
    while endLoop == False:
        
        if savedMsgCount == msgCount:
            endLoop = True
        
        if len(remainingBuf) == 0:
            msg = sConnector.fetchNext()

            if msg.isEmpty():
                logger.debug("Data Stream Ended")
                endLoop = True
                break
            dataToParse = msg.data
        else:
            dataToParse = remainingBuf

        logger.debug("Reading New Stream")
        dataType =  utils.detectType(dataToParse[0:1])

        if dataType == "BIN":
            logger.debug("Entering Binary Mode")
            parserResponse = binaryParser.binaryParsing(dataToParse, sConnector, msg.order)

            # Preserve Data and Relationship to Raw Data
            if (parserResponse.incomplete == False) & (parserResponse.badFetch == False) & (parserResponse.payloadSize == len(parserResponse.payload)):
                responseId = dataWriter.storeBinaryMessage(parserResponse.payload, parserResponse.payloadSize)

                for rawId in parserResponse.reference:
                    dataWriter.storeRelationship(rawId, responseId, "BIN"), 
                savedMsgCount = savedMsgCount + 1
            elif (parserResponse.incomplete == True) & (parserResponse.badFetch == False):
                print("Content {parserResonse.reference} is incomplte, but next msg is different type")
            else:
                logger.warning("Unexpected issue when parsing [{parserResonse.reference}]")
            
            # Process the remaining message in next loop if not empty
            remainingBuf = parserResponse.remainingPayload

        elif dataType == "ASCII":
            logger.debug("Entering ASCII Mode")        
            # extractedBuf, remainingBuf, status = asciiParsing(dataToParse)
            
            parserResponse = asciiParser.asciiParsing(dataToParse, sConnector, msg.order)
            if parserResponse.validMsg:

                payload = parserResponse.payload.decode("ascii")
                if len(payload) >= 5:
                    responseId = dataWriter.storeAsciiMessage(payload)
                    savedMsgCount = savedMsgCount + 1
                    for rawId in parserResponse.reference:
                        dataWriter.storeRelationship(rawId, responseId, "ASCII")
                else:
                    logger.debug("Malformed Message [{payload}] has less than 5 characters")
            
            if (len(parserResponse.remainingPayload) != 0):
                remainingBuf = parserResponse.remainingPayload
            else:
                remainingBuf = bytearray()
        else:
            logger.debug("Unexpected Message Received")
            remainingBuf = bytearray()
    

