import socket as sock
import struct
import random


class SocketWrapper:
    def __init__(self, args):
        self._host = ''
        self._timeout = args.wait
        self._address = args.address
        self._port = random.choice(range(33434, 33535))
        self._socket = self.create_socket()

    def create_socket(self):
        socket = sock.socket(sock.AF_INET, sock.SOCK_RAW, sock.IPPROTO_ICMP)
        socket.settimeout(self._timeout)
        socket.bind((self._host, self._port))
        return socket

    def send_data(self, packet):
        self._socket.sendto(packet, (self._address, self._port))

    def get_data(self):
        return self._socket.recvfrom(1024)

    def close(self):
        self._socket.close()

    def set_socket_options(self, ttl):
        self._socket.setsockopt(sock.IPPROTO_IP, sock.IP_TTL, struct.pack('I', ttl))
