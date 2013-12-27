import StringIO
import pickle

from tornado import ioloop
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


class PickledStreamReader(object):
    def __init__(self, callback):
        self.callback = callback
        self.buffer = StringIO.StringIO()
    
    def feed(self, data):
        pos = self.buffer.tell()
        self.buffer.seek(0, 2)
        self.buffer.write(data)
        self.buffer.seek(pos)
        try:
            obj = pickle.load(self.buffer)
        except (EOFError, ValueError):
            self.buffer.seek(pos)
        else:
            self.callback(obj)


class BackendConnection(object):
    def __init__(self, stream):
        self.stream = stream
        self.reader = PickledStreamReader(self.object_received)
        self.read_next_byte()
    
    def read_next_byte(self):
        self.stream.read_bytes(1, self.data_received) 

    def data_received(self, data):
        self.reader.feed(data)
        self.read_next_byte()
        
    def object_received(self, obj):
        print obj


class BackendServer(tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        BackendConnection(stream)
    

def main():
    CommandServer().listen(1234)
    BackendServer().listen(3456)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
