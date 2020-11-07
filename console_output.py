class ConsoleOutput:
    def __init__(self, args):
        self.args = args
        self.start = (f'Tracing route to {args.host} ({args.address}). ' +
                      f'Max hops: {args.hops}. Packets per ttl: {args.packets}\n')
        self.end = 'Tracing complete!'
        self.output = [self.start]
        self.line = []

    def add_ttl_number(self, ttl):
        return str(ttl).rjust(len(str(self.args.hops)))

    def add_line(self, line):
        self.line.append(line)
        if line[-1] == '\n':
            self._update()

    def _update(self):
        string = ' '.join(self.line)
        self.output.append(string)
        self.line = []

    def print(self):
        for i in self.output:
            print(i, end='')
        print(self.end)
