from model_bakery.recipe import Recipe, foreign_key

from agrotoxico.models import Agrotoxico, TipoAgrotoxico, Espera
from cultura.tests.recipes import cultura

tipo_agrotoxico = Recipe(TipoAgrotoxico)

agrotoxico = Recipe(Agrotoxico, tipo=foreign_key(tipo_agrotoxico))

espera = Recipe(Espera, cultura=foreign_key(cultura), agrotoxico=foreign_key(agrotoxico))
