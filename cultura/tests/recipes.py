from model_bakery.recipe import Recipe, foreign_key

from cultura.models import Cultura, Espera
from agrotoxico.tests.recipes import agrotoxico


cultura = Recipe(Cultura)

espera = Recipe(Espera, cultura=foreign_key(cultura), agrotoxico=foreign_key(agrotoxico))
