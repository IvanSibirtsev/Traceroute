import argparse


def create_args():
    parser = argparse.ArgumentParser(
        description='Python3.8 implementation of traceroute utility. ' +
                    'Read "README.md" for more information')
    parser.add_argument('host', type=str,
                        help='Destination to which utility traces route')
    parser.add_argument('-w', '--wait', type=int,
                        default=1, dest='wait', action='store',
                        help='Time to wait for a response')
    parser.add_argument('-z', type=int, default=0,
                        dest='pause', action='store',
                        help='Pause time between probes')
    parser.add_argument('-m', '--max', type=int,
                        default=64, dest='hops', action='store',
                        help='Max "ttl"')
    parser.add_argument('-s', '--start', type=int,
                        default=1, dest='start', action='store',
                        help='First time-to-live value')
    return parser.parse_args()
