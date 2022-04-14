from model_bakery.recipe import Recipe, foreign_key

from talhao.models import Talhao

from propriedade.tests.recipes import propriedade

talhao = Recipe(Talhao, idPropriedade=foreign_key(propriedade))
