import socket as sock


class CreateSocket:
    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = self.create_socket()

    def create_socket(self):
        socket = sock.socket(sock.AF_INET, sock.SOCK_RAW, sock.IPPROTO_ICMP)
        socket.settimeout(self.timeout)
        socket.bind((self.host, self.port))
        return socket
