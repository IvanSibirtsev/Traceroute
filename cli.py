from Utils.debugger import debug_decorator


class CommandLineInterface:
    def __init__(self, args):
        self.args = args
        self.start = (f'Tracing route to {args.host} ({args.address}). ' +
                      f'Max hops: {args.hops}. Packets per ttl: ' +
                      f'{args.query_number}\n')
        self.end = 'Tracing complete!'
        self.output = [self.start]
        self.line = []

    @debug_decorator
    def add_ttl_number(self, ttl):
        string = str(ttl).rjust(len(str(self.args.hops)))
        self.add_line(string)

    @debug_decorator
    def add_line(self, line):
        self.line.append(line)
        if line[-1] == '\n':
            self._update()

    @debug_decorator
    def _update(self):
        string = ' '.join(self.line)
        self.output.append(string)
        print(string, end='')
        self.line = []

    @debug_decorator
    def print(self):
        print(self.end)
