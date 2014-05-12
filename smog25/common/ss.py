"""ScoreStorage interface."""
from sqlalchemy.orm import exc

from smog25.ss import access
from smog25.ss import schema


class Error(Exception):
    pass


class UniversumNotFoundError(Error):
    pass


class ScoreDB(object):
    """Database class."""

    def __init__(self, path):
        """Creates database access object.

        Args:
            path: Path to database as string.
        """
        self._new_session = access.get_bound_session_class(path)

    def put_score(self, team_name, game_name, universum_name, score):
        """Adds new score.

        Args:
            team_name: Team name as string.
            game_name: Game name as string.
            universum_name: Universum name as string.
            score: Total team score as float.
        """
        session = self._new_session()
        universum = schema.Universum.find_or_create(session, game_name,
                                                    universum_name)
        team = schema.Team.find_or_create(session, team_name)
        new_score = schema.Score.find_or_create(session, team, universum)
        new_score.value = score
        session.add(new_score)
        session.commit()

    def get_scores(self, game, universum):
        """Returns scores for all teams for a particular universum.

        Args:
            game: Game id as string.
            universum: Universum name as string.

        Returns:
            List of (string, float) tuples with team name and its score.
        
        Raises:
            UniversumNotFoundError
        """
        try:
            uni = schema.Universum.find(self._new_session(), game, universum)
        except exc.NoResultFound:
            raise UniversumNotFoundError
        else:
            return [(score.team.name, score.value) for score in uni.scores]
        

    def list_universes(self):
        """Returns list of all stored universes.

        Returns:
            List of (string, string) tuples with game and universum names.
        """
        return self._new_session().query(schema.Universum.game_name,
                                         schema.Universum.universum_name).all()
