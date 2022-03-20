from model_bakery.recipe import Recipe, foreign_key

from propriedade.models import Propriedade

from produtor.tests.recipes import produtor

from tecnico.tests.recipes import tecnico


propriedade = Recipe(
    Propriedade, produtor=foreign_key(produtor), tecnico=foreign_key(tecnico))
