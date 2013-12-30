"""Module for reading contest description files."""
import yaml


class ContestDescription(object):
    """Contest description as loaded from config file.
    
    Assigns each constructor argument to an attribute of the same name.
    Creates dict from argument 'teams', mapping team names to passwords.
    """
    def __init__(self, teams, **kwargs):
        self.team_pass = dict(teams)
        for name, value in kwargs.iteritems():
            setattr(self, name, value)


def load_contest_description(path):
    """Reads YAML contest description file.
    
    Args:
        path: Path to file.
    
    Returns:
        ContestDescription instance.
    """
    with open(path) as conffile:
        return ContestDescription(**yaml.load(conffile))
