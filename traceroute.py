import socket as s
import sys
from Utils.arguments import Arguments
from cli import CommandLineInterface
from Utils.debugger import debug_decorator
from Utils.socket_wrapper import SocketWrapper
from ICMP.ICMP_packet import ICMP
from packet_tracer import PacketTracer


class Traceroute:
    def __init__(self, args, cli, socket):
        self._args = args
        self._cli = cli
        self._address = self._args.address
        self._ttl = 1
        self._sequence = list(range(1, self._args.query_number + 1))
        self._socket = socket

    @debug_decorator
    def start(self):
        received_address = ''
        while self._ttl < self._args.hops and received_address != self._address:
            self._cli.add_ttl_number(self._ttl)
            name, received_address = self._send_packets()
            self._sequence = self._make_sequence()
            self._cli.add_line(name + '\n')
            self._ttl += 1
        return self._cli

    @debug_decorator
    def _make_sequence(self):
        return list(map(lambda n: n + self._args.query_number,
                        self._sequence))

    @debug_decorator
    def _send_packets(self):
        name = ''
        received_address = ''
        for i in range(self._args.query_number):
            icmp = ICMP(self._sequence[i], self._args)
            self._socket.set_socket_options(self._ttl)
            packet = icmp.get_packet()
            packet_tracer = PacketTracer(self._socket, self._sequence,
                                         self._cli, self._args.interval)

            name, received_address = packet_tracer.trace_packet(packet, name)
        return name, received_address


def main():
    args = Arguments()
    cli = CommandLineInterface(args)
    socket = SocketWrapper(args)
    traceroute = Traceroute(args, cli, socket)
    result = traceroute.start()
    result.print()
    socket.close()


if __name__ == '__main__':
    main()
