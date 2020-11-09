data = {'normal': b'E\xc0\x008\x03T\x00\x00\xff\x01\x9f\xa0\n\x00\x02\x02\n'
                  b'\x00\x02\x0f\x0b\x00|#\x00\x00\x00\x00E\x00\x00<\x9cY@'
                  b'\x00\x01\x01~l\n\x00\x02\x0fW\xfa\xfa\xf2\x08\x00gE'
                  b'\t\x96\x00\x01',
        'blocked': b'E\x10\x008\x10\xac\x00\x00\xfb\x01\x0eR\xc3\xd0\xd0'
                   b'\xd7\n\x00\x02\x0f\x03\x01\xa3\x11\x00\x00\x00\x00E'
                   b'\x00<\x00\xfd\xc4\x00@\x07\x01V\xd8\n\x00\x02\x0f\xd9'
                   b'\xc5r\x17\x08\x00\x8c\xca\x90?\x00\x18'}


class TestArgs:
    def __init__(self, adders='', host='', interval=0, query_number=1,
                 timeout=1, hops=10, debug=False, debug_wait=0.1,
                 payload_size=32, from_file=''):
        self.address = adders
        self.host = host
        self.interval = interval
        self.query_number = query_number
        self.timeout = timeout
        self.hops = hops
        self.debug = debug
        self.debug_wait = debug_wait
        self.payload_size = payload_size
        self.from_file = from_file


class TestSocket:
    def __init__(self, args, resource_type='normal'):
        self._host = ''
        self._timeout = args.timeout
        self._address = args.address
        self._port = 10000
        self._socket = object
        self._data = (data[resource_type], ('localhost', 0))

    def create_socket(self):
        return self._socket

    def send_data(self, packet):
        pass

    def get_data(self):
        return self._data

    def set_socket_options(self, ttl):
        pass


class TestCLI:
    def __init__(self, args):
        self._args = args
        self.cli = []

    def add_ttl_number(self, ttl):
        self.cli.append(ttl)

    def add_line(self, new_inf):
        if new_inf.find('ms') == -1:
            self.cli.append(new_inf)

    def print(self):
        self.cli.append('end.')
