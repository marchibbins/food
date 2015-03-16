from flask import session


def append_to_session(key, value):
    """ Gets or creates a session-stored list for given key,
    appends new value and returns updated list. """
    if session.get(key):
        session[key].append(value)
    else:
        session[key] = [value]
    return session[key]


def remove_from_session(key, value):
    """ Removes a value from session if exists, returns True or False. """
    if value in session.get(key):
        session[key].remove(value)
        return True
    else:
        return False


def unique_append_to_session(key, value):
    """ Extends `append_to_session`, enforcing uniqueness. """
    if value in session.get(key, []):
        return session[key]
    else:
        return append_to_session(key, value)
