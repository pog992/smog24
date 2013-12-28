from tornado import ioloop

from smog25.cfe import backend
from smog25.cfe import command
from smog25.cfe import util


def main():
    util.start_server(command.CommandConnection, 1234)
    util.start_server(backend.BackendConnection, 3456)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
