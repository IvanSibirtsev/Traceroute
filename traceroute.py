import socket as s
import sys
from Utils.arguments import Arguments
from console_output import ConsoleOutput
from Utils.debugger import debugger
from Utils.socket_wrapper import SocketWrapper
from ICMP.ICMP_packet import ICMP
from packet_tracer import PacketTracer


class Traceroute:
    def __init__(self, args, output, socket):
        self.args = args
        self.output = output
        self.address = self.args.address
        self.ttl = 1
        self.sequence = list(range(1, self.args.query_number + 1))
        self.socket = socket

    @debugger
    def traceroute(self):
        received_address = ''
        while self.ttl < self.args.hops and received_address != self.address:
            self.output.add_ttl_number(self.ttl)
            name, received_address = self._send_packets()
            self.sequence = self._make_sequence()
            self.output.add_line(name + '\n')
            self.ttl += 1
        return self.output

    @debugger
    def _make_sequence(self):
        return list(map(lambda n: n + self.args.query_number,
                        self.sequence))

    @debugger
    def _send_packets(self):
        name = ''
        received_address = ''
        for i in range(self.args.query_number):
            icmp = ICMP(self.sequence[i], self.args)
            self.socket.set_socket_options(self.ttl)
            packet = icmp.get_packet()
            packet_tracer = PacketTracer(self.socket, self.sequence,
                                         self.output, self.args.interval)

            name, received_address = packet_tracer.trace_packet(packet, name)
        return name, received_address


def main():
    args = Arguments()
    output = ConsoleOutput(args)
    socket = SocketWrapper(args)
    try:
        traceroute = Traceroute(args, output, socket)
    except PermissionError:
        print('Use sudo.\n')
        sys.exit()
    except s.gaierror:
        print('Unknown destination address.')
        sys.exit()
    result = traceroute.traceroute()
    result.print()
    socket.close()


if __name__ == '__main__':
    main()
