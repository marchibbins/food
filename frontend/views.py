from flask import Blueprint, render_template
from food.models import Recipe
from shortcuts import append_to_session, get_or_404


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


@frontend.route('/recipe/<slug>/save')
def recipe_save(slug):
    """ Saves a recipe to session, or 404. """
    recipe = get_or_404(Recipe, Recipe.slug == slug)
    saved = append_to_session('recipes', recipe.key.urlsafe())
    return render_template('frontend/recipe_detail.html', recipe=recipe, saved=saved)


def frontend_errors(app):
    """ Render generic error templates. """
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
