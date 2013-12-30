import collections
import itertools
from tornado import ioloop

from smog25.cfe import backend
from smog25.cfe import command
from smog25.cfe import util


class Cfe(object):
    def __init__(self):
        self.clients_sequencer = itertools.count()
        self.clients = {}
        self.backends = collections.deque()

    def add_client(self, client, team_name):
        assert client not in self.clients
        connection_id = self.clients_sequencer.next()
        self.clients[client] = connection_id
        self.clients[connection_id] = client

    def remove_client(self, client):
        try:
            del self.clients[client]
        except KeyError:
            pass

    def add_backend(self, backend):
        assert backend not in self.backends
        self.backends.append(backend)

    def remove_backend(self, backend):
        try:
            self.backends.remove(backend)
        except ValueError:
            pass

    def command(self, client, team_name, line):
        connection_id = self.clients[client]
        try:
            backend = self.backends[0]
        except IndexError:
            client.writeln("server error")  # TODO
        else:
            backend.write_object((connection_id, team_name, line))

    def reply(self, backend, obj):
        connection_id, text = obj
        try:
            client = self.clients[connection_id]
        except KeyError:
            pass
        else:
            client.writeln(text)


def main():
    cfe = Cfe()
    util.start_server(command.CommandConnection, 1234, cfe)
    util.start_server(backend.BackendConnection, 3456, cfe)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
