from smog25.cfe import util


class CommandConnection(util.Connection):
    def __init__(self, stream, cfe):
        self.cfe = cfe
        cfe.add_client(self, 'team')
        super(CommandConnection, self).__init__(stream)
    
    def read(self):
        self.stream.read_until('\n', self.line_received)
        
    def line_received(self, line):
        self.cfe.command(self, 'team', line[:-1])
        self.read()

    def writeln(self, text):
        self.stream.write('%s\n' % text)

    def became_closed(self):
        self.cfe.remove_client(self)
