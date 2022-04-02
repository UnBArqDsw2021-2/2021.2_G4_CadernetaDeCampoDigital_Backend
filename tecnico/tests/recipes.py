from core.consts.usuarios import TECNICO

from model_bakery.recipe import Recipe

from tecnico.models import Tecnico


tecnico = Recipe(Tecnico, usuario__tipo=TECNICO, usuario__telefone='5561912345678')
