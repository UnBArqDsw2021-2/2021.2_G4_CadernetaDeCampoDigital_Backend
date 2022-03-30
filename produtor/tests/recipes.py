from core.consts.usuarios import PRODUTOR

from model_bakery.recipe import Recipe

from produtor.models import Produtor


produtor = Recipe(
    Produtor, usuario__tipo=PRODUTOR, usuario__telefone='5561912345678')
