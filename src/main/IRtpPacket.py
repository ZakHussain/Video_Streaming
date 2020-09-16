# Author(s): Zak Hussain 
# Date created: 08/03/2020
# Version: 0.0.1

'''
Special Notes:

(1) Log: Zak Hussain - 08/03/2020
    + In this MVP, the following header fields are set to zero: 
        - Padding (P), bit 2
        - Extension (X), bit 3 
        - Contributing Sources (CC), bits 4 through 7 
        - Marker (M), bit 8 
(2) Log: Zak Hussain - 08/04/2020
    + In this MVP, the 32-bit Contributing Source Idenfier is non-existent
      since the CC field is set to zero. 
'''

'''
Purpose:
The IRtpPacket interface provides basic methods for creating 
an RTP (Real-Time Transport Protocol)

structure of an RTP packet is as follows (bit are the first column): 
|byte 0         | byte 1                |byte 2                  |byte 3
__________________________________________________________________________________________
 0 1|2|3|4 5 6 7|8| 9 10 11 12 13 14 15 | 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+|
| V |P|X|  CC   |M|         PT          |                    Sequence Number             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+|
|                                   TimeStamp                                            |   
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+|
|                        synchronization source (SSRC) identifier                        |   
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+|
|                         Contributing Source (CSRC) identifiers                         |           
|________________________________________________________________________________________|

Components of the packet: 

Header (4 bytes): 
    Version (V): bits 0,1 are used to indicate the verion of the protocol being used. 

    Padding (P): bit 2, is used to indicate whether there are extra padding 
                 at the end of the RTP padding. (Recall padding is necessary 
                 for encryption algorithms or if the block is required to be
                 a certain size.)

    Extension (X): bit 3, indicates existence of 'extension header' between the header
                   and payload.

    Contributing Sources (CC):  bits 4 through 7, contains the number of CSRC identifiers 
                                following the SSRC. 

    Marker (M): bit 8, Signal used at the application level. If set, it means the current data 
                has some relevant/important use in the application 

    Payload Type (PT): bits 9 through 15 (7-bits), is use to indicate the payload's format type. 

    Sequence Number: bits 16 through 31 (16-bits), is used to indicate packet loss at the receiver. 
                    This value is incremented for each RTP packet sent. Note that the initial 
                    sequence number should be random--this is for security purposes. (Think
                    know-plaintext attacks)

Timestamp (4 bytes): 32 bits, and is used for timing when to play back received samples.

Synchronization Source Identifier (SSRC) (4 bytes): 32 bits, This is used to uniquely 
                    identify the source of the stream.

Contributing Source (CSRC) (4 bytes): This is the number of entries indicated by the
                    CSRC count. 

Header Extension (4 bytes): -- not used. 
'''
HEADER_SIZE = 12

class IRtpPacket:
    
    payload = None 

    def encapsulate(self, version: int, padding: int, extension: int, 
                    contr_sources: int, marker: int, payload_type: int, 
                seq_num: int, sync_source_id: int, payload: str) -> None:
        """For the inputs, apply them to the RTP packet fields.""" 
        pass
    
    def decode(self, byteStream: bytes) -> None: 
        """ For use by the client to de-packetize the data"""
        pass 

    def get_seq_num(self) -> int: 
        """ Returns the rtp packet sequence number (frame number)."""
        pass 

    def get_timestamp(self) -> int: 
        """ Returns the timestamp for this RTP packet."""
        pass 

    def get_payload(self) -> bytes: 
        """ Return the payload content from the RTP packet."""
        pass 

    def get_packet(self) -> bytes: 
        """ Returns the contents (header + payload) of the packet itself"""
        pass  



    
