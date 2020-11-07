from arguments import Arguments
from console_output import ConsoleOutput
from socket_wrapper import SocketWrapper
from ICMP.ICMP import ICMP
import socket as s
import sys
from packet_tracer import PacketTracer


class Traceroute:
    def __init__(self, args, output, socket):
        self.args = args
        self.output = output
        self.address = self.args.address
        self.ttl = args.start
        self.sequence = list(range(1, self.args.packets + 1))
        self.socket = socket

    def traceroute(self):
        while self.ttl < self.args.hops:
            self.output.add_ttl_number(self.ttl)
            name, received_address = self._send_packets()
            self.sequence = self._make_sequence()
            self.output.add_line(name + '\n')
            if received_address == self.address:
                break
            self.ttl += 1
        return self.output

    def _make_sequence(self):
        func = lambda n: n + self.args.packets
        return list(map(func, self.sequence))

    def _send_packets(self):
        name = None
        received_address = ''
        for i in range(self.args.packets):
            icmp = ICMP(self.sequence[i])
            self.socket.set_socket_options(self.ttl)
            packet = icmp.get_packet()
            packet_tracer = PacketTracer(self.socket, self.sequence,
                                         self.output, self.args.is_ip)
            name, received_address = packet_tracer.trace_packet(packet, name)
        return name, received_address


def main():
    args = Arguments()
    output = ConsoleOutput(args)
    socket = SocketWrapper(args)
    try:
        traceroute = Traceroute(args, output, socket)
    except PermissionError as e:
        sys.stderr.write(e.strerror + '\n')
        sys.exit(1)
    except s.gaierror:
        sys.stderr.write('Destination address is unknown\n')
        sys.exit(2)
    result = traceroute.traceroute()
    result.print()
    socket.close()


if __name__ == '__main__':
    main()
