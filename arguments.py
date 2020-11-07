import argparse
import socket


class Arguments:
    def __init__(self):
        self._console_args = create_args()
        self.address = socket.gethostbyname(self._console_args.host)
        self.host = self._console_args.host
        self.wait = self._console_args.wait
        self.is_ip = self._console_args.is_ip
        self.packets = self._console_args.packets
        self.timeout = self._console_args.timeout
        self.hops = self._console_args.hops
        self.start = self._console_args.start


def create_args():
    parser = argparse.ArgumentParser(
        description='Python3.8 implementation of traceroute utility. ' +
                    'Read "README.md" for more information')
    parser.add_argument('-host', type=str,
                        default='ya.ru',
                        help='Destination to which utility traces route')
    parser.add_argument('-w', '--wait', type=int,
                        default=1, dest='wait', action='store',
                        help='Time to wait for a response')
    parser.add_argument('-n', '--numerically', action='store_true',
                        dest='is_ip',
                        help='Print addresses only numerically')
    parser.add_argument('-q', '--query', type=int,
                        default=3, dest='packets', action='store',
                        help='Amount of packets per "ttl"')
    parser.add_argument('-z', type=int, default=0,
                        dest='timeout', action='store',
                        help='Pause time between probes')
    parser.add_argument('-m', '--max', type=int,
                        default=64, dest='hops', action='store',
                        help='Max "ttl"')
    parser.add_argument('-s', '--start', type=int,
                        default=1, dest='start', action='store',
                        help='First time-to-live value')
    return parser.parse_args()
