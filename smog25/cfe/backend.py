import StringIO
import pickle

from tornado import tcpserver


class PickledStreamReader(object):
    def __init__(self, callback):
        self.callback = callback
        self.buffer = StringIO.StringIO()
    
    def _append(self, data):
        pos = self.buffer.tell()
        self.buffer.seek(0, 2)
        self.buffer.write(data)
        self.buffer.seek(pos)

    def feed(self, data):
        self._append(data)
        while True:
            pos = self.buffer.tell()
            try:
                obj = pickle.load(self.buffer)
            except (EOFError, ValueError):
                self.buffer.seek(pos)
                self.buffer = StringIO.StringIO(self.buffer.read())
                break
            else:
                self.callback(obj)


class BackendConnection(object):
    def __init__(self, stream):
        self.stream = stream
        self.stream.set_close_callback(self.became_closed)
        self.reader = PickledStreamReader(self.object_received)
        self.read_next_bytes()
    
    def read_next_bytes(self):
        self.stream.read_bytes(4096, self.read_next_bytes, self.reader.feed)

    def object_received(self, obj):
        print obj

    def became_closed(self):
        print 'closed.'

    def write_object(self, obj):
        self.stream.write(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL))


class BackendServer(tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        BackendConnection(stream)
