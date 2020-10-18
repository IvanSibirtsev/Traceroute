import arg_parser
import time
import struct
from output import Output
from network import CreateSocket
from ICMP import ICMP
import socket


class Traceroute:
    def __init__(self, args):
        self.args = args
        self.ttl = args.ttl
        self.sequence = list(range(1, self.args.packets + 1))
        self.socket = CreateSocket(args.host, args.port, args.timeout).socket
        self.address = socket.gethostbyname(args.host)
        self.output = Output(self.args.host, self.address,
                             self.ttl, args.packet)

    def traceroute(self):
        while self.ttl < self.args.hops:

            for i in range(self.args.packets):
                packet = ICMP(self.sequence[i])
                self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,
                                       struct.pack('I', self.ttl))


def main():
    args = arg_parser.create_args()


if __name__ == '__main__':
    main()
