import os
import unittest

from smog25.common import contestdesc


def data_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


SAMPLE_CONF = data_path('sample_contest_desc.yml')


class TestContestDescription(unittest.TestCase):

    def testLoad(self):
        desc = contestdesc.load_contest_description(SAMPLE_CONF)
        self.assertEqual(desc.team_pass,
                         {'Bum Bum City': 'tra, ', 'queueing': 'pass123'})
        self.assertEqual(desc.ss_path, '/var/run/db')


if __name__ == '__main__':
    unittest.main()
