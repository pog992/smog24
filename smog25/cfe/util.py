"""Tornado abstractions and utilities."""
from tornado import tcpserver


class Connection(object):
    """Class representing a TCP connection.

    Registers became_closed to be called on socket closure calls read method.

    Args:
        stream: Tornado IOStream.

    Attrs:
        stream: Tornado IOStream.
    """
    def __init__(self, stream):
        self.stream = stream
        self.stream.set_close_callback(self.became_closed)
        self.read()
    
    def read(self):
        """Orders to read more data from socket."""
        pass
    
    def became_closed(self):
        """Called when connection was closed."""
        pass


def start_server(connection_type, port, *args):
    """Starts new tornado TCPServer.

    Args:
        connection_type: Called on a new connections with tornado IOStream
            and *args as arguments.
        port: Integer.
        *args: Extra arguments passed to connection_type call.
    """
    class Server(tcpserver.TCPServer):
        def handle_stream(self, stream, address):
            connection_type(stream, *args)
    Server().listen(port)
