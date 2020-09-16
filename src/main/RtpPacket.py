# Author(s): Zak Hussain 
# Date created: 08/04/2020
# Version: 0.0.1

"""
Special Notes

The Logic for manipulating the bytestream is used almost exactly the 
same as is provided by the Kurose Lab6 VideoStreaming Assignment. 
"""

"""
Purpose: 

The RtpPacket class is used to create a simple RTP packet. 
It is used by the server to encapsulate the header fields and payload; 
whereas, it provides the client app access to the contents of the packet
via methods such as decode() and the numerous get methods. 
"""
from time import time 
from bitstring import * 
from IRtpPacket import IRtpPacket

BYTE_SIZE = 8
HEADER_SIZE = 12 
MAX_LENGTHS = {
    "version" : 2,
    "padding" : 1,
    "extension" : 1,
    "contr_sources" : 4,
    "marker" : 1,
    "payload_type" : 7, 
    "seq_num" : 16, 
    "sync_source_id" : 32, 
    "timestamp" : 32
}

class RtpPacket(IRtpPacket): 

################ Public methods #####################################
    def encapsulate(self, version: int, padding: int, extension: int, 
                    contr_sources: int, marker: int, payload_type: int, 
                seq_num: int, sync_source_id: int, payload) -> None:
        """For the inputs, apply them to the RTP packet fields.""" 
        
        self.timestamp = int(time()) 
        self.header = bytearray(HEADER_SIZE)
        self.payload = payload

        # 1.CONVERT ALL INPUT TO BINARY OF NEEDED LENGTHS
        version_bin = self.__convert_uint_to_binary(version, MAX_LENGTHS["version"])
        padding_bin = self.__convert_uint_to_binary(padding, MAX_LENGTHS["padding"])
        extension_bin = self.__convert_uint_to_binary(extension, MAX_LENGTHS["extension"])
        contr_sources_bin = self.__convert_uint_to_binary(contr_sources, MAX_LENGTHS["contr_sources"])
        marker_bin = self.__convert_uint_to_binary(marker, MAX_LENGTHS["marker"])
        payload_type_bin = self.__convert_uint_to_binary(payload_type, MAX_LENGTHS["payload_type"]) 
        seq_num_bin = self.__convert_uint_to_binary(seq_num, MAX_LENGTHS["seq_num"]) 
        sync_source_id_bin = self.__convert_uint_to_binary(sync_source_id, MAX_LENGTHS["sync_source_id"])
        timestamp_bin = self.__convert_uint_to_binary(self.timestamp, MAX_LENGTHS["timestamp"])

        # 2.CREATE THE NEEDED BYTESTRINGS for the 12 bytes header
        byte_string_0 = self.__build_bytestring([version_bin, padding_bin, extension_bin, contr_sources_bin])
        byte_string_1 = self.__build_bytestring([marker_bin, payload_type_bin]) 
        byte_string_2_3 = self.__build_bytestring([seq_num_bin]) 
        
        byte_string_4_5_6_7 = self.__build_bytestring([timestamp_bin]) 
        byte_string_8_9_10_11 = self.__build_bytestring([sync_source_id_bin])

        # 3. CONVERT EACH OF THE BYTSTRINGS ABOVE INTO A UINT and insert them into the associated byte in the header byterarray
        self.header[0] = self.__convert_to_unsigned_num(byte_string_0)
        self.header[1] = self.__convert_to_unsigned_num(byte_string_1)
        self.header[2] = self.__convert_to_unsigned_num(byte_string_2_3[0:8])
        self.header[3] = self.__convert_to_unsigned_num(byte_string_2_3[8:])
        self.header[4] = self.__convert_to_unsigned_num(byte_string_4_5_6_7[0:8])
        self.header[5] = self.__convert_to_unsigned_num(byte_string_4_5_6_7[8:16])
        self.header[6] = self.__convert_to_unsigned_num(byte_string_4_5_6_7[16:24])
        self.header[7] = self.__convert_to_unsigned_num(byte_string_4_5_6_7[24:32])
        self.header[8] = self.__convert_to_unsigned_num(byte_string_8_9_10_11[0:8])
        self.header[9] = self.__convert_to_unsigned_num(byte_string_8_9_10_11[8:16])
        self.header[10] = self.__convert_to_unsigned_num(byte_string_8_9_10_11[16:24])
        self.header[11] = self.__convert_to_unsigned_num(byte_string_8_9_10_11[24:32])

    def decode(self, byteStream: bytes) -> None: 
        """ For use by the client to de-packetize the data"""
        self.header = bytearray(byteStream[:HEADER_SIZE])
        self.payload = byteStream[HEADER_SIZE:]
    
    def get_version(self) -> int: 
        return int(self.header[0] >> 6) 

    def get_seq_num(self) -> int: 
        """ Returns the rtp packet sequence number (frame number)."""
        seqNum = self.header[2] << 8 | self.header[3]
        return int(seqNum)

    def get_timestamp(self) -> int: 
        """ Returns the timestamp for this RTP packet."""
        timestamp = (self.header[4] << 24 | self.header[5] << 16 | 
                    self.header[6] << 8 | self.header[7])
        return int(timestamp) 

    def get_payload_type(self) -> int: 
        pt = self.header[1] & 127
        return int(pt)       
        
    def get_payload(self) -> bytes: 
        """ Return the payload content from the RTP packet."""
        return self.payload

    def get_packet(self) -> bytes: 
        """ Returns the contents (header + payload) of the packet itself"""
        return self.header + self.payload 

    ################## Private methods ####################################
    def __convert_to_unsigned_num(self, bytestring:str): 
        """
            Returns an uint representing the given bytestring.
        """
        return BitArray(bin=bytestring).uint

    def __build_bytestring(self, bitstrings: list): 
        """
            Returns a string of 8 bits by concatenating the elements in the
            given bitstring. 
        """
        string = ""
        for bitstring in bitstrings: 
            string = string + bitstring 
        return string     

    def __convert_uint_to_binary(self, num: int, length: int) -> str: 
        """
            returns a bitstring representing a given number and its length. 
        """
        return BitArray(uint=num, length=length).bin

    def __byte_index(self, bit_index: int) -> int: 
        """ Returns the computed byte_index based on the desired bit index
            (chooses the byte). 
        """
        byte_index = bit_index//8
        return byte_index

    def __bit_idx_in_byte(self, bit_index: int) -> int: 
        """ Returns the index of a bit from within a byte (chooses the bit)."""
        bit_idx_in_byte = bit_index % BYTE_SIZE
        return bit_idx_in_byte

    def __byte_mask(self, bit_in_byte_idx: int) -> int:
        """ Returns an 8-bit value ranging [128, 1]"""
        num_shifts = 7 - bit_in_byte_idx 
        byte_mask = (1 << num_shifts) 
        return byte_mask

    def __bit_is_set(self, byte_stream: bytearray, byte_idx: int, mask: int) -> bool: 
        """ 
            Returns true if the particular byte contains a 1 at the position marked
            by the mask
        """
        return (byte_stream[byte_idx] & mask) != 0

    def __set_bits_on(self, byte_stream: bytearray, byte_index: int, mask: int) -> None: 
        """
            Updates the byte_stream with a 1 bit depending upon a masking value
        """
        byte_stream[byte_index] |= mask 

    def __set_bits_off(self, byte_stream: bytearray, byte_index: int, mask: int) -> None: 
        """
            Updates the byte_stream with a 0 bit depending upon a masking value
        """    
        byte_stream[byte_index] &= ~mask

    def __toggle_bits(self, byte_stream: bytearray, byte_index: int, mask: int) -> None: 
        """
            Updates the byte_stream with a 0 bit depending upon a masking value
        """    
        byte_stream[byte_index] ^= mask

    def __compute_byte_value(self, int_list: list) -> int: 
        """
            Returns an int sum from a list of ints. The integers are 
            the rtp field values that will be contained in a single byte. 
        """
        return sum(int_list)

    def __str__(self): 
        return ("version: " + str(self.get_version()) + ", "
                "sequence_number: " + str(self.get_seq_num()) + ", "
                "timestamp: " + str(self.get_timestamp()) + ", "
                "payload: " + str(self.get_payload( )))