from flask import abort, session


def append_to_session(key, value):
    """ Gets or creates a session stored list for given key,
    appends new value and returns updated list """
    key_list = session.get(key, [])
    key_list.append(value)
    return key_list


def get_or_404(klass, *args, **kwargs):
    """ Gets an object or raises 404. """
    instance = klass.query(*args, **kwargs).get()
    if not instance:
        abort(404)
    else:
        return instance
