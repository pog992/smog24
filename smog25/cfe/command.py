"""Module dealing with contestants' connections."""
from smog25.cfe import util


class CommandConnection(util.Connection):
    """Connection with contestant.

    Args:
        stream: Tornado IOStream.
        cfe: cfe.Cfe instane.
    """
    def __init__(self, stream, cfe):
        self.cfe = cfe
        cfe.add_client(self, 'team')
        super(CommandConnection, self).__init__(stream)
    
    def read(self):
        self.stream.read_until('\n', self._line_received)
        
    def _line_received(self, line):
        self.cfe.command(self, 'team', line[:-1])
        self.read()

    def write(self, text):
        """Sends text to contestant.

        Args:
            text: String.
        """
        self.stream.write(text)

    def became_closed(self):
        self.cfe.remove_client(self)
