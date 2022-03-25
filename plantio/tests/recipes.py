from cultura.models import Cultura

from model_bakery.recipe import Recipe, foreign_key

from plantio.models import Plantio

from talhao.models import Talhao


plantio = Recipe(
    Plantio, talhao=foreign_key(Talhao), cultura=foreign_key(Cultura))
