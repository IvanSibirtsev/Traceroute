import socket as sock
import struct
import sys
import random
from Utils.debugger import debug_decorator


class SocketWrapper:
    def __init__(self, args):
        self._host = ''
        self._timeout = args.timeout
        self._address = args.address
        self._port = random.choice(range(33434, 33535))
        self._socket = self.create_socket()

    @debug_decorator
    def create_socket(self):
        try:
            socket = sock.socket(sock.AF_INET, sock.SOCK_RAW, sock.IPPROTO_ICMP)
        except PermissionError:
            print('Use sudo.\n')
            sys.exit()
        socket.bind((self._host, self._port))
        return socket

    @debug_decorator
    def send_data(self, packet):
        self._socket.sendto(packet, (self._address, self._port))

    @debug_decorator
    def get_data(self):
        self._socket.settimeout(self._timeout)
        data = self._socket.recvfrom(1024)
        return data

    @debug_decorator
    def close(self):
        self._socket.close()

    @debug_decorator
    def set_socket_options(self, ttl):
        ttl_count = struct.pack('I', ttl)
        self._socket.setsockopt(sock.IPPROTO_IP, sock.IP_TTL, ttl_count)
