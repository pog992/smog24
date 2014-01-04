"""Module dealing with connection to Game Backend."""
import StringIO
import pickle

from smog25.cfe import util


class PickledStreamReader(object):
    """Reads incoming bytes and unpickles objects.

    Args:
        callback: Function to be called when an object is found,
            with it as a sole argument.
    """
    def __init__(self, callback):
        self._callback = callback
        self._buffer = StringIO.StringIO()
    
    def _append(self, data):
        """Appends new data to buffer levaing file position intact.

        Args:
            data: String.
        """
        pos = self._buffer.tell()
        self._buffer.seek(0, 2)
        self._buffer.write(data)
        self._buffer.seek(pos)

    def feed(self, data):
        """Adds new input data to stream.

        Args:
            data: String.
        """
        self._append(data)
        while True:
            pos = self._buffer.tell()
            try:
                obj = pickle.load(self._buffer)
            except (EOFError, ValueError):
                self._buffer.seek(pos)
                self._buffer = StringIO.StringIO(self._buffer.read())
                break
            else:
                self._callback(obj)


class BackendConnection(util.Connection):
    """Connection with Game Backend.

    Args:
        stream: Tornado IOStream.
        cfe: cfe.Cfe instance.
    """
    def __init__(self, stream, cfe):
        self.cfe = cfe
        cfe.add_backend(self)
        self.reader = PickledStreamReader(self._object_received)
        super(BackendConnection, self).__init__(stream)
    
    def read(self):
        self.stream.read_bytes(4096, self.read, self.reader.feed)

    def _object_received(self, obj):
        self.cfe.reply(self, obj)

    def write_object(self, obj):
        """Pickles and sends object.

        Args:
            obj: Object to be sent.
        """
        self.stream.write(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL))

    def became_closed(self):
        self.cfe.remove_backend(self)
