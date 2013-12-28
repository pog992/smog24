from smog25.cfe import util


class CommandConnection(util.Connection):
    def __init__(self, stream):
        super(CommandConnection, self).__init__(stream)
    
    def read(self):
        self.stream.read_until('\n', self.line_received)
        
    def line_received(self, line):
        self.stream.write('> %s' % line)
        if line != 'quit\n':
            self.read()
