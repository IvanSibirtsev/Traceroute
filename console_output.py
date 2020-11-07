from Utils.debugger import debugger

class ConsoleOutput:
    def __init__(self, args):
        self.args = args
        self.start = (f'Tracing route to {args.host} ({args.address}). ' +
                      f'Max hops: {args.hops}. Packets per ttl: ' +
                      f'{args.query_number}\n')
        self.end = 'Tracing complete!'
        self.output = [self.start]
        self.line = []

    @debugger
    def add_ttl_number(self, ttl):
        string = str(ttl).rjust(len(str(self.args.hops)))
        self.add_line(string)

    @debugger
    def add_line(self, line):
        self.line.append(line)
        if line[-1] == '\n':
            self._update()

    @debugger
    def _update(self):
        string = ' '.join(self.line)
        self.output.append(string)
        print(string, end='')
        self.line = []

    @debugger
    def print(self):
        print(self.end)
