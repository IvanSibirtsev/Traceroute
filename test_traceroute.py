import unittest
import sys
import io
import os
from test_classes import TestArgs, TestCLI, TestSocket
from ICMP import ICMP_packet as ICMPPacket
from ICMP import payload
from Utils import debugger
import cli
import packet_tracer
import traceroute


class TestPayload(unittest.TestCase):
    def test_random(self):
        args = TestArgs(payload_size=40)
        payload_test = payload.Payload(args).get_payload()
        self.assertEqual(32, len(payload_test))

    def test_from_file(self):
        message = '123456'
        test_file = 'test_txt'
        with open(test_file, 'w') as file:
            file.write(message)
        args = TestArgs(from_file=test_file)
        payload_test = payload.Payload(args).get_payload()
        self.assertEqual(len(message), len(payload_test))
        os.remove(test_file)


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
        console = TestCLI(args)
        pack_tracer = packet_tracer.PacketTracer(socket, [1], console, 0.05)
        name, received_address = pack_tracer.trace_packet(icmp_packet, '')
        self.assertEqual(received_address, 'localhost')

    def test_blocked(self):
        args = TestArgs()
        ICMPPacket.ICMP.ID = 0
        icmp_packet = ICMPPacket.ICMP(1, args).get_packet()
        socket = TestSocket(args, 'blocked')
        console = TestCLI(args)
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
        right = ['test_classes.TestArgs object', 'binary data']
        self.assertEqual(func_arg, right)
        self.assertEqual(returned_val, right)

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
        cli_test = cli.CommandLineInterface(args)
        cli_test.add_ttl_number(1)
        cli_test.add_line('line\n')
        cli_test.print()
        right = ' 1 line\nTracing complete!\n'
        sys.stdout = old_stdout
        cli_test = buffer.getvalue()
        self.assertEqual(cli_test, right)


class TestTraceroute(unittest.TestCase):
    def test_traceroute(self):
        args = TestArgs(adders='localhost')
        socket = TestSocket(args)
        cli_test = TestCLI(args)
        ICMPPacket.ICMP.ID = 2454
        traceroute_test = traceroute.Traceroute(args, cli_test, socket)
        traceroute_test.start()
        right = [1, 'localhost (localhost)\n']
        self.assertEqual(cli_test.cli, right)


if __name__ == '__main__':
    unittest.main()
