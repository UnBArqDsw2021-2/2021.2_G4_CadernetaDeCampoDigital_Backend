from cultura.tests.recipes import cultura

from model_bakery.recipe import Recipe, foreign_key

from plantio.models import Plantio

from talhao.tests.recipes import talhao


plantio = Recipe(
    Plantio, talhao=foreign_key(talhao), cultura=foreign_key(cultura))
