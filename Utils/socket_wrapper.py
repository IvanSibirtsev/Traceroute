import socket as sock
import struct
import random
import time
from Utils.debugger import debugger


class SocketWrapper:
    def __init__(self, args):
        self._host = ''
        self._timeout = args.timeout
        self._address = args.address
        self._port = random.choice(range(33434, 33535))
        self._socket = self.create_socket()

    @debugger
    def create_socket(self):
        socket = sock.socket(sock.AF_INET, sock.SOCK_RAW, sock.IPPROTO_ICMP)

        socket.bind((self._host, self._port))
        return socket

    @debugger
    def send_data(self, packet):
        self._socket.sendto(packet, (self._address, self._port))

    @debugger
    def get_data(self):
        self._socket.settimeout(self._timeout)
        data = self._socket.recvfrom(1024)
        return data

    @debugger
    def close(self):
        self._socket.close()

    @debugger
    def set_socket_options(self, ttl):
        ttl_count = struct.pack('I', ttl)
        self._socket.setsockopt(sock.IPPROTO_IP, sock.IP_TTL, ttl_count)
