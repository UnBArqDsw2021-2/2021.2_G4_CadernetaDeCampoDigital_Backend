from model_bakery.recipe import Recipe

from produtor.models import Produtor

from usuario.models import Usuario


produtor = Recipe(
    Produtor, usuario__tipo=Usuario.PRODUTOR, usuario__telefone='5561912345678')
