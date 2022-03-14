from model_bakery.recipe import Recipe

from usuario.models import Usuario


# FIXME: Por conta do tipo obrigatório, esse usuário está sendo
# criado com um tipo fixo e pré-definido, mesmo não sendo um
usuario = Recipe(Usuario, telefone='5561912345678', _fill_optional=True)
