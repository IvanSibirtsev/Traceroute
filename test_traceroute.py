import unittest
import sys
import io

from test_classes import TestArgs, TestOutput, TestSocket
import ICMP.ICMP_packet as ICMPPacket
import ICMP.payload as payload
import Utils.arguments as arguments
import Utils.debugger as debugger
import Utils.output_code
import console_output
import packet_tracer
import traceroute


class TestPayload(unittest.TestCase):
    def test_random(self):
        args = TestArgs(payload_size=40)
        payload_test = payload.Payload(args).get_payload()
        self.assertEqual(32, len(payload_test))

    def test_from_file(self):
        message = '123456'
        with open('test.txt', 'w') as file:
            file.write(message)
        args = TestArgs(from_file='test.txt')
        payload_test = payload.Payload(args).get_payload()
        self.assertEqual(len(message), len(payload_test))


class TestICMPPacket(unittest.TestCase):
    def test_len(self):
        args = TestArgs(payload_size=40)
        icmp = ICMPPacket.ICMP(1, args).get_packet()
        self.assertEqual(40, len(icmp))


class TestPacketTracer(unittest.TestCase):
    def test_normal(self):
        args = TestArgs()
        ICMPPacket.ICMP.ID = 2454
        icmp_packet = ICMPPacket.ICMP(1, args).get_packet()

        socket = TestSocket(args)
        console = TestOutput(args)
        pack_tracer = packet_tracer.PacketTracer(socket, [1], console, 0.05)
        name, received_address = pack_tracer.trace_packet(icmp_packet, '')
        self.assertEqual(received_address, 'localhost')

    def test_blocked(self):
        args = TestArgs()
        ICMPPacket.ICMP.ID = 0
        icmp_packet = ICMPPacket.ICMP(1, args).get_packet()
        socket = TestSocket(args, 'blocked')
        console = TestOutput(args)
        seq = [22, 23, 24]
        pack_tracer = packet_tracer.PacketTracer(socket, seq, console, 0.05)
        name, received_address = pack_tracer.trace_packet(icmp_packet, '')
        self.assertEqual(received_address, 'localhost')


class TestDebugger(unittest.TestCase):
    def test_args(self):
        args = TestArgs()
        func_arg = tuple([args, b'1234'])
        returned_val = tuple([args, b'1234'])
        reformat_args = debugger.ReformatArguments(func_arg, returned_val)
        func_arg = reformat_args.get_reformat_function_arguments()
        returned_val = reformat_args.get_reformat_returned_value()
        self.assertEqual(func_arg, ['test_classes.TestArgs object', 'binary data'])
        self.assertEqual(returned_val, ['test_classes.TestArgs object', 'binary data'])

    def test_void_functions(self):
        args = TestArgs()
        func_arg = tuple([args, b'1234'])
        reformat_args = debugger.ReformatArguments(func_arg, None)
        returned_val = reformat_args.get_reformat_returned_value()
        self.assertEqual(returned_val, 'void function')

    def test_unary_functions(self):
        func_args = 'some arg'
        reformat_args = debugger.ReformatArguments(func_args, None)
        func_args = reformat_args.get_reformat_function_arguments()
        self.assertEqual(func_args, ['some arg'])


class TestConsoleOutput(unittest.TestCase):
    def test_add(self):
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        args = TestArgs()
        output = console_output.ConsoleOutput(args)
        output.add_ttl_number(1)
        output.add_line('line\n')
        output.print()
        right = ' 1 line\nTracing complete!\n'
        sys.stdout = old_stdout
        output = buffer.getvalue()
        self.assertEqual(output, right)


class TestTraceroute(unittest.TestCase):
    def test_traceroute(self):
        args = TestArgs(adders='localhost')
        socket = TestSocket(args)
        output = TestOutput(args)
        ICMPPacket.ICMP.ID = 2454
        traceroute_test = traceroute.Traceroute(args, output, socket)
        traceroute_test.traceroute()
        right = [1, 'localhost (localhost)\n']
        self.assertEqual(output.output, right)


if __name__ == '__main__':
    unittest.main()
