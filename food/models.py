from flask import abort
from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    """ Adds shortcut methods to `ndb.Model` for get and ordered fetch. """
    @classmethod
    def fetch_all(cls):
        return cls.query().order(cls.slug)

    @classmethod
    def get_or_404(cls, slug):
        """ Gets an object or raises 404. """
        instance = cls.query(cls.slug == slug).get()
        if not instance:
            abort(404)
        else:
            return instance


class Measures():
    """ Units of measure. """
    GRAMS = 'g'
    MILLILITRES = 'ml'
    UNITS = 'units'
    choices = (GRAMS, MILLILITRES, UNITS)


class Ingredient(BaseModel):
    """ Represents a single ingredient. """
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True, indexed=True)
    measure = ndb.StringProperty(required=True, choices=Measures.choices)


class Quantity(ndb.Model):
    """ Represents an amount of ingredients. """
    ingredient = ndb.KeyProperty(Ingredient, required=True)
    amount = ndb.IntegerProperty(required=True)

    @property
    def measured_amount(self):
        measure = self.ingredient.get().measure
        if measure == Measures.UNITS:
            return self.amount
        else:
            return '%d%s' % (self.amount, measure)


class Recipe(BaseModel):
    """ Represents a single recipe, with multiple quantities. """
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True, indexed=True)
    method = ndb.TextProperty()
    quantities = ndb.StructuredProperty(Quantity, repeated=True)
