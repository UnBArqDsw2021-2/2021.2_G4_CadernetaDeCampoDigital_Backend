from model_bakery.recipe import Recipe, foreign_key

from plantio.models import Plantio

from talhao.models import Talhao


plantio = Recipe(
    Plantio, produtor=foreign_key(Talhao))
