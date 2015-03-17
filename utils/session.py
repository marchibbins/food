from flask import session


def append_to_session(key, value):
    """ Gets or creates a session-stored list for given key,
    appends new value and returns updated list. """
    if session.get(key):
        session[key].append(value)
    else:
        session[key] = [value]
    return session[key]


def get_session_list(key):
    """ Gets list from session or returns empty list. """
    return session.get(key, [])


def in_session_list(key, value):
    """ Checks whether value is in session list. """
    return value in get_session_list(key)


def remove_from_session(key, value):
    """ Removes a value from session if exists, returns True or False. """
    if in_session_list(key, value):
        session[key].remove(value)
        return True
    else:
        return False


def unique_append_to_session(key, value):
    """ Extends `append_to_session`, enforcing uniqueness. """
    if in_session_list(key, value):
        return session[key]
    else:
        return append_to_session(key, value)
