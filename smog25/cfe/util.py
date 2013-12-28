from tornado import tcpserver

class Connection(object):
    def __init__(self, stream):
        self.stream = stream
        self.stream.set_close_callback(self.became_closed)
        self.read()
    
    def read(self):
        pass
    
    def became_closed(self):
        print self, "closed"


def start_server(connection_type, port, *args):
    class Server(tcpserver.TCPServer):
        def handle_stream(self, stream, address):
            connection_type(stream, *args)
    Server().listen(port)
