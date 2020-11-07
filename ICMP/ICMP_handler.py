from Utils.output_code import OutputType
from ICMP.ICMP import ICMP
import struct


class ICMPHandler:
    def __init__(self, sequence, data):
        self._pack_header = self._unpack_packet_header(data[20:28])
        self._type = self._pack_header[0]
        self._sequence = sequence
        self._data = data
        self._output_code = None
        self._delegator = {0: self._zero_type,
                           3: self._third_type,
                           11: self._eleven_type}
        self._handle()

    def get_output_code(self):
        return self._output_code

    def _handle(self):
        return self._delegator[self._type]()

    def _zero_type(self):
        if (self._pack_header[3] == ICMP.ID
                and self._pack_header[4] in self._sequence):
            self._output_code = OutputType.SUCCESS.value

    def _third_type(self):
        code = self._pack_header[1]
        if code == 0:
            self._output_code = OutputType.NET.value
        elif code == 1:
            self._output_code = OutputType.HOST.value
        elif code in (9, 10, 13):
            self._output_code = OutputType.PROHIB.value
        else:
            self._output_code = '!{code}'

    def _eleven_type(self):
        inner_header = self._unpack_packet_header(self._data[48:56])
        if (inner_header[0] == 8 and
                inner_header[3] == ICMP.ID and
                inner_header[4] in self._sequence):
            self._output_code = OutputType.SUCCESS.value

    @staticmethod
    def _unpack_packet_header(data):
        return struct.unpack('!BBHHH', data)
