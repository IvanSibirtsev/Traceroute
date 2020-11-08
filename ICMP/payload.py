import random


class Payload:
    def __init__(self, args):
        packet_header_length = 8
        self._size = args.payload_size - packet_header_length
        self._file = args.from_file

    def get_payload(self):
        if self._file:
            return self._get_payload_from_file()
        else:
            return self._random_byte_message()

    def _get_payload_from_file(self):
        with open(self._file, 'rb') as payload_file:
            return payload_file.read()

    def _random_byte_message(self):
        sequence = random.choices(
            b'abcdefghijklmnopqrstuvwxyz'
            b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            b'1234567890', k=self._size)
        return bytes(sequence)
