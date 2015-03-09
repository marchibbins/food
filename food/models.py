from google.appengine.ext import ndb


class Ingredient(ndb.Model):
    name = ndb.StringProperty(required=True)
    measure_choices = ('grams', 'ml', 'units')
    measure = ndb.StringProperty(choices=measure_choices, required=True)


class Quantity(ndb.Model):
    ingredient = ndb.StructuredProperty(Ingredient, required=True)
    amount = ndb.IntegerProperty(required=True)


class Recipe(ndb.Model):
    name = ndb.StringProperty(required=True)
    method = ndb.TextProperty()
    quantities = ndb.StructuredProperty(Quantity, repeated=True)
