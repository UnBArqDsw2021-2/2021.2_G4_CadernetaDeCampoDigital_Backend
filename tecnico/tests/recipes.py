from model_bakery.recipe import Recipe

from tecnico.models import Tecnico

from usuario.models import Usuario


tecnico = Recipe(Tecnico, usuario__tipo=Usuario.TECNICO, usuario__telefone='5561912345678')
