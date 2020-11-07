from output_code import OutputType
import time
import socket as s
from ICMP.ICMP_handler import ICMPHandler


class PacketTracer:
    def __init__(self, socket, sequence, output,  is_ip):
        self._socket = socket
        self._output = output
        self._sequence = sequence
        self._is_ip = is_ip
        self._output_code = None
        self._start_time = time.perf_counter()

    def trace_packet(self, packet, name):
        self._socket.send_data(packet)
        self._output_code = OutputType.ERROR.value
        while self._output_code == OutputType.ERROR.value:
            (received_address, d_time,
             self._output_code) = self._get_information_about_packet()
            if received_address:
                self._time_add(d_time)
            if self._output_code != OutputType.ERROR.value:
                self._output.add_line(self._reformat_output_code())
            if self._output_code == '*':
                if name is None:
                    name = 'Packet receiving timeout'
            elif (received_address is not None and
                  self._output_code != OutputType.ERROR.value):
                try:
                    received_host = s.gethostbyaddr(received_address)[0] + ' '
                except s.error:
                    received_host = f'{received_address} '
                if self._is_ip:
                    received_host = ''
                name = f'{received_host}({received_address})'
        return name, received_address

    def _get_information_about_packet(self):
        d_time = 0
        try:
            data, received_address = self._socket.get_data()
            d_time = (time.perf_counter() - self._start_time) * 1000
            received_address = received_address[0]
            output_code = ICMPHandler(self._sequence, data).get_output_code()
        except s.timeout:
            received_address = None
            output_code = '*'
        return received_address, d_time, output_code

    def _time_add(self, d_time):
        if self._output_code.startswith('!'):
            self._output_code = f'{str(d_time)[:5]}ms {self._output_code}'
        if self._output_code == OutputType.SUCCESS.value:
            self._output_code = f'{str(d_time)[:5]}ms'

    def _reformat_output_code(self):
        return self._output_code.ljust(8)
