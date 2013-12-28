import StringIO
import pickle

from smog25.cfe import util


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


class BackendConnection(util.Connection):
    def __init__(self, stream):
        self.reader = PickledStreamReader(self.object_received)
        super(BackendConnection, self).__init__(stream)
    
    def read(self):
        self.stream.read_bytes(4096, self.read, self.reader.feed)

    def object_received(self, obj):
        print obj

    def write_object(self, obj):
        self.stream.write(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL))
