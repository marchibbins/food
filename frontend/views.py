from flask import Blueprint, render_template
from food.models import Recipe


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def recipe_list():
    """ Render a list of recipes. """
    recipes = Recipe.query().fetch()
    return render_template('frontend/recipe_list.html', recipes=recipes)
