from google.appengine.ext import ndb
import json

from food.models import Ingredient, Measures, Quantity, Recipe


def resetdb():
    """ Quick delete and reload of database. """
    try:
        delete()
        load_json()
        return 'Data reset'
    except Exception as error:
        return '%s' % error


def delete():
    """ Deletes all Ingredients and Recipes. """
    ndb.delete_multi(
        Ingredient.query().fetch(keys_only=True) +
        Recipe.query().fetch(keys_only=True)
    )


def load_json():
    """ Attempt to parse and put from JSON. """
    # Ingredients
    ingredients_file = open('json/ingredients.json')
    ingredients_json = json.load(ingredients_file)

    slugs = map(lambda i: i['slug'], ingredients_json)
    if len(slugs) != len(set(slugs)):
        raise Exception('Duplicate ingredients found in JSON')

    ingredients = {}
    for ingredient in ingredients_json:
        for prop in ['name', 'slug', 'measure']:
            if not ingredient.get(prop):
                raise Exception('Ingredient missing %s' % prop)
        slug = ingredient['slug']
        if ingredient['measure'] not in Measures.choices:
            raise Exception('"%s" not in measures' % ingredient['measure'])
        if Ingredient.query(Ingredient.slug == slug).get():
            raise Exception('Ingredient "%s" already exists' % slug)
        ingredients[slug] = Ingredient(name=ingredient['name'],
                                       slug=slug,
                                       measure=ingredient['measure'])
    ingredients_file.close()
    ndb.put_multi(ingredients.values())

    # Recipes
    recipes_file = open('json/recipes.json')
    recipes_json = json.load(recipes_file)

    slugs = map(lambda i: i['slug'], recipes_json)
    if len(slugs) != len(set(slugs)):
        raise Exception('Duplicate recipes found in JSON')

    recipes = []
    for recipe in recipes_json:
        for prop in ['name', 'slug']:
            if not recipe.get(prop):
                raise Exception('Recipe missing %s' % prop)
        if Recipe.query(Recipe.slug == recipe['slug']).get():
            raise Exception('Recipe "%s" already exists' % recipe['slug'])
        quantities = []
        for quantity in recipe['quantities']:
            for prop in ['slug', 'amount']:
                if not quantity.get(prop):
                    raise Exception('Quantity missing %s' % prop)
            slug = quantity['slug']
            if not ingredients.get(slug):
                raise Exception('Ingredient "%s" not found' % slug)
            quantities.append(Quantity(ingredient=ingredients[slug].key,
                                       amount=quantity['amount']))
        recipes.append(Recipe(name=recipe['name'],
                              slug=recipe['slug'],
                              method=recipe.get('method', ''),
                              quantities=quantities))
    recipes_file.close()
    ndb.put_multi(recipes)
