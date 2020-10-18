import random
import struct


class ICMP:
    ID = random.randint(0, 65535)

    def __init__(self, seq_num):
        self.id = self.ID
        self.seq_num = seq_num
        self.packet = self.create_packet()

    def create_packet(self):
        icmp_header = struct.pack('!BBHHH', 8, 0, 0, self.id, self.seq_num)
        icmp_data = struct.pack('!QQQQQL', 2, 0, 0, 0, 0, 0)
        packet = icmp_header + icmp_data
        checksum = self.make_checksum(packet)
        icmp_header = struct.pack('!BBHHH', 8, 0, checksum,
                                  self.id, self.seq_num)

        return icmp_header + icmp_data

    @staticmethod
    def set_id():
        return random.randint(0, 65535)

    @staticmethod
    def make_checksum(packet):
        unpacked = struct.unpack('!LLLLLLLLLLLLL', packet)
        res = sum(unpacked)
        res += (res >> 16)
        return ~res & 0xffff
