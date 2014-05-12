"""Tests for smog25.common.ss and whole SS module."""
import unittest
from smog25.ss import access
from smog25.common import ss


class TestScoreDB(unittest.TestCase):

    @staticmethod
    def new_db():
        """Returns ScoreDB instance of in-memory database."""
        return ss.ScoreDB(access.IN_MEMORY_DATABASE_PATH)

    def test_empty(self):
        db = self.new_db()
        self.assertEqual(db.list_universes(), [])

    def test_get_single_score(self):
        db = self.new_db()
        db.put_score('team1', 'game', '1', 123)
        db.put_score('team1', 'game', '1', 127)
        self.assertItemsEqual(db.get_scores('game', '1'), [('team1', 127)])

    def test_list_universes(self):
        db = self.new_db()
        db.put_score('team1', 'game', '1', 1.5)
        db.put_score('team2', 'game', '2', 2)
        db.put_score('team2', 'game', '1', 3)
        self.assertItemsEqual(sorted(db.list_universes()),
                              [('game', '1'), ('game', '2')])

    def test_get_multiple_score(self):
        db = self.new_db()
        db.put_score('team1', 'game', '1', 1.5)
        db.put_score('team2', 'game', '1', 2)
        db.put_score('team2', 'game', '1', 3)
        self.assertItemsEqual(sorted(db.get_scores('game', '1')),
                              [('team1',  1.5), ('team2', 3)])

    def test_universum_not_found(self):
        db = self.new_db()
        self.assertRaises(ss.UniversumNotFoundError,
                          lambda: db.get_scores("game", "universum"))


if __name__ == "__main__":
    unittest.main()
