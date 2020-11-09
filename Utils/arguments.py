import argparse
import socket
import sys
import os


class Arguments:
    def __init__(self):
        self._console_args = create_args()
        self.address = self._get_address()
        self.host = self._console_args.host
        self.interval = self._console_args.interval
        self.query_number = self._console_args.query_number
        self.timeout = self._console_args.timeout
        self.hops = self._console_args.hops
        self.debug = self._console_args.debug
        self.debug_wait = self._console_args.debug_wait
        self.payload_size = self._console_args.payload_size
        self.from_file = self._console_args.from_file
        self._check_payload_length()
        self._check_path()

    def _get_address(self):
        try:
            return socket.gethostbyname(self._console_args.host)
        except socket.gaierror:
            print('Unknown destination address.')
            sys.exit()

    def _check_payload_length(self):
        icmp_header_len = 8
        if self.payload_size <= icmp_header_len:
            print(f'Payload size must be > {icmp_header_len}.')
            sys.exit()

    def _check_path(self):
        if self.from_file and not os.path.exists(self.from_file):
            print(f'No such file {self.from_file}')
            sys.exit()


def create_args():
    helper = {
        'host': 'Destination to which utility traces route.',
        'debug': 'Debug mode.',
        'debug_wait':
            'The interval in seconds between debugger messages.',
        'interval':
            'The interval in seconds between sending each packet.',
        'query_number': 'Number of packets per "ttl"',
        'timeout':
            'The maximum waiting time for receiving a reply in seconds.',
        'max': 'Maximum "ttl"',
        'size': 'The payload size. Ignored when "-file" used.',
        'file': 'The file with payload data.'
    }

    parser = argparse.ArgumentParser(
        description='Python3.8 implementation of traceroute utility. ' +
                    'Read "README.md" for more information')
    parser.add_argument('-host', type=str, default='ya.ru',
                        help=helper['host'])
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        dest='debug', help=helper['debug'])
    parser.add_argument('-dw', '--debug_wait', type=float,
                        default=0.1, dest='debug_wait', action='store',
                        help=helper['debug_wait'])
    parser.add_argument('-i', '--interval', type=float, default=0.05,
                        dest='interval', action='store',
                        help=helper['interval'])
    parser.add_argument('-qn', '--query_number', type=int,
                        default=3, dest='query_number', action='store',
                        help=helper['query_number'])
    parser.add_argument('-t', type=float, default=2,
                        dest='timeout', action='store',
                        help=helper['timeout'])
    parser.add_argument('-m', '--max', type=int,
                        default=64, dest='hops', action='store',
                        help=helper['max'])
    parser.add_argument('-s', '--size', type=int,
                        default=40, dest='payload_size', action='store',
                        help=helper['size'])
    parser.add_argument('-f', '--from_file', type=str,
                        default='', dest='from_file',
                        help=helper['file'])
    return parser.parse_args()
