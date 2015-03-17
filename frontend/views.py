from flask import abort, Blueprint, flash, redirect, render_template, \
    request, url_for

from google.appengine.ext import ndb
from itertools import chain

from food.models import Ingredient, Quantity, Recipe
from food.parser import resetdb
from utils.session import get_session_list, in_session_list, \
    remove_from_session, unique_append_to_session


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def recipe_list():
    """ Render a list of recipes. """
    recipes = Recipe.fetch_all()
    return render_template('frontend/recipe_list.html', recipes=recipes)


@frontend.route('/recipe/<slug>')
def recipe_detail(slug):
    """ Render a recipe matching a slug, or 404. """
    recipe = Recipe.get_or_404(slug)
    saved = in_session_list('recipes', recipe.key.urlsafe())
    return render_template('frontend/recipe_detail.html',
                           recipe=recipe, saved=saved)


@frontend.route('/ingredients/')
def ingredient_list():
    """ Render a list of ingredients. """
    ingredients = Ingredient.fetch_all()
    return render_template('frontend/ingredient_list.html',
                           ingredients=ingredients)


@frontend.route('/ingredients/<slug>')
def ingredient_detail(slug):
    """ Render a ingredient matching a slug, or 404. """
    ingredient = Ingredient.get_or_404(slug)
    recipes = Recipe.query(Recipe.quantities.ingredient == ingredient.key)
    return render_template('frontend/ingredient_detail.html',
                           ingredient=ingredient, recipes=recipes)


@frontend.route('/recipe/<slug>/<action>', methods=['GET', 'POST'])
def recipe_action(slug, action):
    """ Save or remove a recipe to or from session, or 404. """
    if action not in ['save', 'remove']:
        abort(404)
    recipe = Recipe.get_or_404(slug)
    if request.method == 'POST':
        if action == 'save':
            update = unique_append_to_session
        else:
            update = remove_from_session
        if update('recipes', recipe.key.urlsafe()):
            flash(u'Recipe %sd' % action)
        else:
            flash(u'Unable to %s recipe' % action)
        return redirect(url_for('frontend.recipe_detail', slug=slug))
    else:
        return render_template('frontend/recipe_action.html', recipe=recipe,
                               action=action)


@frontend.route('/saved')
def saved():
    """ Render a list of saved recipes and collate ingredients. """
    recipe_keys = map(lambda string: ndb.Key(urlsafe=string),
                      get_session_list('recipes'))
    recipes = filter(None, ndb.get_multi(recipe_keys))
    quantities = {}
    for quantity in list(chain.from_iterable(
                           map(lambda recipe: recipe.quantities, recipes))):
        key = quantity.ingredient.urlsafe()
        if quantities.get(key):
            quantities[key].amount += quantity.amount
        else:
            quantities[key] = Quantity(ingredient=quantity.ingredient,
                                       amount=quantity.amount)
    return render_template('frontend/saved.html', recipes=recipes,
                           quantities=quantities)


@frontend.route('/resetdb')
def dummy_data():
    """ Resets database, returns True or False. """
    return resetdb()


def frontend_errors(app):
    """ Render generic error templates. """
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
