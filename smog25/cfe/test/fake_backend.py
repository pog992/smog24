import pickle
import socket
import sys


def handle(obj):
    connection_id, _team_name, line = obj
    return connection_id, "[%s]" % line


def main(host, port_str):
    sock = socket.socket()
    sock.connect((host, int(port_str)))
    sockfile = sock.makefile('r+', 0)
    pickler = pickle.Pickler(sockfile)
    unpickler = pickle.Unpickler(sockfile)
    while True:
        pickler.dump(handle(unpickler.load()))


if __name__ == '__main__':
    try:
        main(*sys.argv[1:])
    except TypeError:
        print>>sys.stderr, "usage: %s host port" % sys.argv[0]
    except (EOFError, KeyboardInterrupt):
        pass
