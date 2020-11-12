from Utils.debugger import debug_decorator


class CommandLineInterface:
    def __init__(self, args):
        self._args = args
        self._start = (f'Tracing route to {args.host} ({args.address}). ' +
                       f'Max hops: {args.hops}. Packets per ttl: ' +
                       f'{args.query_number}\n')
        self._end = 'Tracing complete!'
        self._output = [self._start]
        self._line = []

    @debug_decorator
    def add_ttl_number(self, ttl):
        string = str(ttl).rjust(len(str(self._args.hops)))
        self.add_line(string)

    @debug_decorator
    def add_line(self, line):
        self._line.append(line)
        if line[-1] == '\n':
            self._update()

    @debug_decorator
    def _update(self):
        string = ' '.join(self._line)
        self._output.append(string)
        print(string, end='')
        self._line = []

    @debug_decorator
    def print(self):
        print(self._end)
