from tornado import tcpserver


class CommandConnection(object):
    def __init__(self, stream):
        self.stream = stream
        self.stream.set_close_callback(self.became_closed)
        self.read_next_line()
    
    def read_next_line(self):
        self.stream.read_until('\n', self.line_received)
        
    def line_received(self, line):
        self.stream.write('> %s' % line)
        if line != 'quit\n':
            self.read_next_line()
    
    def became_closed(self):
        print 'closed.'


class CommandServer(tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        CommandConnection(stream)
    