from google.appengine.ext import ndb


class Ingredient(ndb.Model):
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(indexed=True)
    measure_choices = ('grams', 'ml', 'units')
    measure = ndb.StringProperty(choices=measure_choices, required=True)

    @classmethod
    def fetch_all(klass):
        return klass.query().order(Ingredient.slug).fetch()


class Quantity(ndb.Model):
    ingredient = ndb.StructuredProperty(Ingredient, required=True)
    amount = ndb.IntegerProperty(required=True)


class Recipe(ndb.Model):
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(indexed=True)
    method = ndb.TextProperty()
    quantities = ndb.StructuredProperty(Quantity, repeated=True)

    @classmethod
    def fetch_all(klass):
        return klass.query().order(Recipe.slug).fetch()
