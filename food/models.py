from flask import abort
from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    """ Adds shortcut methods to `ndb.Model` for get and ordered fetch. """
    @classmethod
    def fetch_all(cls):
        return cls.query().order(Ingredient.slug).fetch()

    @classmethod
    def get_or_404(cls, slug):
        """ Gets an object or raises 404. """
        instance = cls.query(cls.slug == slug).get()
        if not instance:
            abort(404)
        else:
            return instance


class Ingredient(BaseModel):
    """ Represents a single ingredient. """
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(indexed=True)
    measure_choices = ('grams', 'ml', 'units')
    measure = ndb.StringProperty(choices=measure_choices, required=True)


class Quantity(ndb.Model):
    """ Represents an amount of ingredients. """
    ingredient = ndb.StructuredProperty(Ingredient, required=True)
    amount = ndb.IntegerProperty(required=True)


class Recipe(BaseModel):
    """ Represents a single recipe, with multiple quantities. """
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(indexed=True)
    method = ndb.TextProperty()
    quantities = ndb.StructuredProperty(Quantity, repeated=True)
