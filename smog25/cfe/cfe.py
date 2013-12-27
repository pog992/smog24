from tornado import ioloop

from smog25.cfe import backend
from smog25.cfe import command


def main():
    command.CommandServer().listen(1234)
    backend.BackendServer().listen(3456)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
