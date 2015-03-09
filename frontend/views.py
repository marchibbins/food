from flask import Blueprint, render_template
from food.models import Recipe


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    """ Render a list of recipes. """
    recipes = Recipe.query().fetch()
    return render_template('index.html', recipes=recipes)
