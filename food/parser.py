from google.appengine.ext import ndb

from food.models import Ingredient, Measures, Quantity, Recipe


def resetdb():
    """ Quick delete and reload of database. """
    if delete() and put():
        return "Data reset"
    else:
        return "Something went wrong"


def delete():
    """ Deletes all Ingredients and Recipes. """
    return ndb.delete_multi(
        Ingredient.query().fetch(keys_only=True) +
        Recipe.query().fetch(keys_only=True)
    )


def put():
    """ Puts all dummy Ingredients and Recipes. """
    one = Ingredient(name='One', slug='one', measure=Measures.GRAMS)
    two = Ingredient(name='Two', slug='two', measure=Measures.MILLILITRES)
    three = Ingredient(name='Three', slug='three', measure=Measures.UNITS)
    ndb.put_multi([
        one,
        two,
        three,
    ])
    return ndb.put_multi([
        Recipe(name='A', slug='a', quantities=[
            Quantity(ingredient=one.key, amount=10),
            Quantity(ingredient=two.key, amount=12),
            Quantity(ingredient=three.key, amount=5),
        ]),
        Recipe(name='B', slug='b', quantities=[
            Quantity(ingredient=one.key, amount=3),
        ]),
    ])
