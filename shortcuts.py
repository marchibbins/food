from flask import abort


def get_or_404(klass, *args, **kwargs):
    """ Gets an object or raises 404. """
    instance = klass.query(*args, **kwargs).get()
    if not instance:
        abort(404)
    else:
        return instance
