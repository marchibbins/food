from flask import Blueprint, flash, redirect, render_template, session, url_for
from google.appengine.ext import ndb
from food.models import Ingredient, Recipe
from shortcuts import unique_append_to_session, get_or_404


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def recipe_list():
    """ Render a list of recipes. """
    recipes = Recipe.query().fetch()
    return render_template('frontend/recipe_list.html', recipes=recipes)


@frontend.route('/recipe/<slug>')
def recipe_detail(slug):
    """ Render a recipe matching a slug, or 404. """
    recipe = get_or_404(Recipe, Recipe.slug == slug)
    return render_template('frontend/recipe_detail.html', recipe=recipe)


@frontend.route('/ingredients/')
def ingredient_list():
    """ Render a list of ingredients. """
    ingredients = Ingredient.query().fetch()
    return render_template('frontend/ingredient_list.html',
                           ingredients=ingredients)


@frontend.route('/ingredients/<slug>')
def ingredient_detail(slug):
    """ Render a ingredient matching a slug, or 404. """
    ingredient = get_or_404(Ingredient, Ingredient.slug == slug)
    return render_template('frontend/ingredient_detail.html',
                           ingredient=ingredient)


@frontend.route('/recipe/<slug>/save', methods=['POST'])
def recipe_save(slug):
    """ Saves a recipe to session, or 404. """
    recipe = get_or_404(Recipe, Recipe.slug == slug)
    if unique_append_to_session('recipes', recipe.key.urlsafe()):
        flash(u'Recipe saved')
    else:
        flash(u'Unable to save recipe')
    return redirect(url_for('frontend.recipe_detail', slug=slug))


@frontend.route('/saved')
def saved():
    """ Render a list of saved recipes. """
    recipes = ndb.get_multi(map(lambda string: ndb.Key(urlsafe=string),
                                session.get('recipes', [])))
    return render_template('frontend/recipe_list.html', recipes=recipes)


@frontend.route('/reload')
def dummy_data():
    """ Adds dummy data for development. """
    from google.appengine.ext import ndb
    from food.models import Quantity

    # Out with the old
    ndb.delete_multi(Ingredient.query().fetch(keys_only=True))
    ndb.delete_multi(Recipe.query().fetch(keys_only=True))

    # In with the new
    one = Ingredient(name='One', slug='one', measure='grams')
    two = Ingredient(name='Two', slug='two', measure='ml')
    three = Ingredient(name='Three', slug='three', measure='units')
    ndb.put_multi([
        one, two, three
    ])
    ndb.put_multi([
        Recipe(name='A', slug='a', quantities=[
            Quantity(ingredient=one, amount=10),
            Quantity(ingredient=two, amount=12),
            Quantity(ingredient=three, amount=5)
        ]),
        Recipe(name='B', slug='b', quantities=[
            Quantity(ingredient=one, amount=3)
        ]),
    ])

    return "Data loaded"


def frontend_errors(app):
    """ Render generic error templates. """
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
