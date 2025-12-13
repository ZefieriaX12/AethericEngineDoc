# AI was used to get the range of printable ASCII
from connector.SConnector import SConnector
import parser.Utils as utils

import logging
logger = logging.getLogger(__name__)


class AsciiParserResponse:
    payload: bytearray
    remainingPayload: bytearray
    reference: list[int]
    validMsg: bool

    def __init__(self, payload, remainingPayload, references, validMsg):
        self.payload = payload
        self.remainingPayload = remainingPayload
        self.reference = references
        self.validMsg = validMsg

# AI was used to get the range
def isPrintableAscii(code:int):
    if 32 <= code <= 126:
        return True
    return False

def asciiParsing(data:bytes,sConn: SConnector, refId: int, starterChar="$", terminatorChar=";"):
    
    msgToPreserve = bytearray()
    endLoop = False
    validMsg = True
    startPreserving = False
    
    byteToLoop = bytearray(data)
    references = []
    references.append(refId)
    
    while endLoop == False:

        if (len(byteToLoop) == 0) & (startPreserving == False):
            endLoop == True
            break
        elif (len(byteToLoop) == 0) & (startPreserving == True):
            # Still recording but reach end of message and final char is not ";", fetch next msg
            nextMsg = sConn.fetchNext()
            if isPrintableAscii(nextMsg.data[0]):

                byteToLoop = bytearray(nextMsg.data)
                references.append(nextMsg.order)
            else:
                # Message does not contains printable ascii, assume that message is invalid
                validMsg = False
                return AsciiParserResponse(msgToPreserve, nextMsg.data, references, validMsg)
        byteNum = byteToLoop.pop(0)
        
        if (byteNum == starterChar.encode()[0]) & (startPreserving == False):
            # Start $ detected, start recording payload
            startPreserving = True
        elif startPreserving & (byteNum == terminatorChar.encode()[0]):
            # End of message reach, ending loop, any remaining data, next loop will handle it
            endLoop = True
            startPreserving = False

        elif startPreserving & isPrintableAscii(byteNum):         
            msgToPreserve.append(byteNum)
        elif startPreserving & (not isPrintableAscii(byteNum)):
            # Non printable char found, assume message is bad... Still loop till ";" is reached...
            msgToPreserve.append(byteNum)
            validMsg = False
        else:
            logger.warning("Unexpected ASCII Extraction Reached. Status[Preserving={startPreserving}, Parsing={data}]")
        
    return AsciiParserResponse(msgToPreserve, byteToLoop, references, validMsg)

# def asciiParsing(initialData:bytes,sConn: SConnector, refId:int, starterChar="$", terminatorChar=";"):
    
#     extractedMsg = None
#     remainingMsg = None
#     validMsg = None
    
#     if (initialData[0] == starterChar.encode()[0]):
#         extractedMsg, remainingMsg, validMsg = extractTillTerminator(initialData,sConn,refId, starterChar, terminatorChar)
#     else:
#         remainingMsg = bytearray(initialData)
#         validMsg = False
   
#     logger.debug(f"Original: [{initialData}]")
#     logger.debug(f"Remaining: [{remainingMsg}]" )
#     logger.debug(f"Msg To preserve: [{extractedMsg}]")

#     return extractedMsg, remainingMsg, validMsg