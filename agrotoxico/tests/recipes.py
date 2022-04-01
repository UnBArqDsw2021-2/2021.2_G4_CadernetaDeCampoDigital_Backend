from model_bakery.recipe import Recipe, foreign_key

from agrotoxico.models import Agrotoxico, TipoAgrotoxico

tipo_agrotoxico = Recipe(TipoAgrotoxico)

agrotoxico = Recipe(Agrotoxico, tipo=foreign_key(tipo_agrotoxico))
