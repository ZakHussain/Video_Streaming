'''
* Class for RTSP Request Object
* Fields
- fileName, str: filename if media gets written to file
- seqNum, int: RTSP sequence number
- reqType, str: RTSP request type, mirrors RTSP states (init, play, etc.)
- rtpPort, int: the port the client wants to run RTP connection

> Example use (sep python file, i.e. the server. I'm unclear if de-pickling the request object means you have access to the obj fields w/o importing the
parent class (i.e. import RstpRequest as rq?) Either way, this is the idea:

#-------recv'ing access to the obj------#
# import or....
import RstpRequest as rq

# do de-pickling, whatever that code is
newRequest = dumps(recievedRequestObject)


#-------getting access to fields: uses @property under the hood------#
reqRecvd = newRequest.reqType
print(reqRecvd)
print(newRequest.seqNum)
print(newRequest.fileName)

#update the field: code under @xxx.setter decorator will ensure update safety, like using enums

# would work
newRequest.reqType = 'pause'

# would fail under @reqType.setter logic
newRequest.reqType = 'not a valid command'

'''

VALIDREQS = ["SETUP", "PLAY", "PAUSE", "TEARDOWN"]

class RtspRequest:


    def __init__(self, reqType, seqNum, fileName, rtpPort):
        self.rtpPort = rtpPort
        if type(reqType) is str and type(fileName) is str:
            self.reqType = reqType
            self.fileName= fileName
        else:
            raise TypeError("reqType and filename must be str")

        if reqType not in VALIDREQS:
            raise ValueError("invalid req types")           

        if type(seqNum) is int and seqNum > 0:
            self.seqNum = seqNum
        else:
            raise TypeError("seqNum must be a int > 0")

    @property
    def reqType(self):
        return self.__reqType

    
    @reqType.setter
    def reqType(self, reqType):
        if reqType in VALIDREQS:
            self.__reqType = reqType
        else:
            raise ValueError("invalid request type")
    
    @property
    def fileName(self):
        return self.__fileName

    @fileName.setter
    def fileName(self, fileName):
        if type(fileName) is str:
            self.__fileName = fileName
    
    @property
    def seqNum(self):
        return self.__seqNum
    
    # as of now, blocks <0 seqNums, can add other logic
    @seqNum.setter
    def seqNum(self, seqNum):
        if seqNum < 1:
            raise ValueError("Seq must be > 0")
        else:
            self.__seqNum = seqNum

    @property
    def rtpPort(self):
        return self.__rtpPort

    @rtpPort.setter
    def rtpPort(self, port):
        # if port > 16385 and port < 16000:
        #     raise ValueError("port must be <= 16384 and > 16000")
        # else:
        self.__rtpPort = port

    def __str__(self):
        return "Req Type: " + self.reqType +  " Seq Num: " + str(self.seqNum) + " File name: " + self.fileName + " RTP Port: " + str(self.rtpPort) 
    
    