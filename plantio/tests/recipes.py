from agrotoxico.tests.recipes import agrotoxico

from cultura.tests.recipes import cultura

from model_bakery.recipe import Recipe, foreign_key

from plantio.models import Plantio, AplicacaoAgrotoxico

from talhao.tests.recipes import talhao


plantio = Recipe(
    Plantio, talhao=foreign_key(talhao), cultura=foreign_key(cultura))


aplicacao = Recipe(
    AplicacaoAgrotoxico, plantio=foreign_key(plantio), agrotoxico=foreign_key(agrotoxico))
