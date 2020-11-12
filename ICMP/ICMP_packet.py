import random
import struct
from ICMP.payload import Payload


class ICMP:
    ID = random.randint(0, 65535)

    def __init__(self, seq_num, args):
        self._seq_num = seq_num
        self._args = args
        self._packet = self._create_packet()

    def _create_packet(self):
        icmp_header = struct.pack('!BBHHH', 8, 0, 0, self.ID, self._seq_num)
        payload = Payload(self._args).get_payload()
        packet = icmp_header + payload
        checksum = self._make_checksum(packet)
        icmp_header = struct.pack('!BBHHH', 8, 0, checksum,
                                  self.ID, self._seq_num)
        return icmp_header + payload

    def get_packet(self):
        return self._packet

    @staticmethod
    def _make_checksum(data):
        checksum = 0
        data += b'\x00'
        for i in range(0, len(data) - 1, 2):
            checksum += (data[i] << 8) + data[i + 1]
            checksum = (checksum & 0xffff) + (checksum >> 16)
        checksum = ~checksum & 0xffff
        return checksum
