import unittest

import ICMP.ICMP_packet
import ICMP.ICMP_handler
import ICMP.payload
import Utils.arguments
import Utils.debugger
import Utils.output_code
import Utils.socket_wrapper
import console_output
import packet_tracer
import traceroute


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
