"""Database schema definitions."""
from sqlalchemy.ext import declarative
from sqlalchemy.orm import exc
from sqlalchemy import Column
from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types


Base = declarative.declarative_base()


class Universum(Base):
    """Instance of game with a particular configuration."""
    __tablename__ = 'universum'
    __table_args__ = (schema.Index('universum_index', 'game_name',
                                   'universum_name', unique=True),
                     )
    
    id = Column(types.Integer, primary_key=True)
    game_name = Column(types.String, nullable=False)
    universum_name = Column(types.String, nullable=False)

    def __repr__(self):
        return '%s:%s' % (self.game_name, self.universum_name)
    
    @staticmethod
    def find(session, game_name, universum_name):
        """
        Searches for a Universum of the given game and universum name.

        Args:
            session: Sqlalchemy session.
            game_name: Game name as string.
            universum_name: Universum name as string.

        Raises:
            sqlalchemy.exc.NoResultFound: When none is found.

        Returns:
            Universum
        """
        return session.query(Universum).filter(
                Universum.game_name==game_name,
                Universum.universum_name==universum_name).one()
    
    @classmethod
    def find_or_create(cls, session, game_name, universum_name):
        """
        Searches for a Universum of the given game and universum name.
        If none is found, a new one is created.

        Args:
            session: Sqlalchemy session.
            game_name: Game name as string.
            universum_name: Universum name as string.

        Returns:
            Universum
        """
        try:
            return cls.find(session, game_name, universum_name)
        except exc.NoResultFound:
            uni = Universum(game_name=game_name, universum_name=universum_name)
            session.add(uni)
            return uni


class Team(Base):
    """Contestant with a unique name."""
    __tablename__ = 'team'
    __table_args__ = (schema.Index('team_index', 'name', unique=True), )
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String, nullable=False)
    
    def __repr__(self):
        return 'Team(%s)' % self.name
    
    @staticmethod
    def find_or_create(session, name):
        """
        Searches for team of the given name. Creates new one if necessary.

        Args:
            session: Sqlalchemy session.
            name: Team name as string.

        Returns:
            Team
        """
        try:
            return session.query(Team).filter(Team.name==name).one()
        except exc.NoResultFound:
            team = Team(name=name)
            session.add(team)
            return team

    
class Score(Base):
    """Current team score in a particular universum."""
    __tablename__ = 'score'
    __table_args__ = (schema.Index('score_index', 'universum_id', 'team_id',
                                   unique=True),
                     )
    
    id = Column(types.Integer, primary_key=True)
    universum_id = Column(types.Integer, schema.ForeignKey('universum.id'),
                          nullable=False)
    team_id = Column(types.Integer, schema.ForeignKey('team.id'),
                     nullable=False)
    value = Column(types.Float, nullable=False)
    
    universum = orm.relationship("Universum", backref="scores")
    team = orm.relationship("Team", backref="teams")
    
    @staticmethod
    def find_or_create(session, team, universum):
        """Searches for Score entry for a given team and universum.
        If none is found, a new one is created.

        Args:
            session: Sqlalchemy session.
            team: Team instance.
            universum: Universum instance.

        Returns:
            Score
        """
        try:
            return session.query(Score).filter(
                Score.team==team, Score.universum==universum).one()
        except exc.NoResultFound:
            score = Score(team=team, universum=universum)
            session.add(score)
            return score
    
    
class ScoreHist(Base):
    """History of score changes."""
    __tablename__ = 'scorehist'
    
    id = Column(types.Integer, primary_key=True)
    score_id = Column(types.Integer, schema.ForeignKey('score.id'),
                      nullable=False)
    time = Column(types.DateTime, nullable=False)
    change = Column(types.Float, nullable=False)
    
    score = orm.relationship('Score', backref='scores')
    