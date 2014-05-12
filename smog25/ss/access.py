"""Module with utilities for accessing database."""
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from smog25.ss import schema


IN_MEMORY_DATABASE_PATH = ''


def get_bound_session_class(path, initialize=True):
    """Initializes database schema and returns bound Session class.

    Args:
        path: Path to database file as string.
        initialize: Whether to create db schema.

    Returns:
        Session class bound to database, as returned by sessionmaker.
    """
    engine = sqlalchemy.create_engine('sqlite://%s' % path)
    if initialize:
        base = schema.Base
        base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
