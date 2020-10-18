
class Output:
    def __init__(self, host, address, hops, packets):
        self.start = (f'Tracing route to {host} ({address}). ' +
                f'Max hops: {hops}. Packets per ttl: {packets}')
        self.output = [self.start]

    def add(self, new_information):
        self.output.append(new_information)
