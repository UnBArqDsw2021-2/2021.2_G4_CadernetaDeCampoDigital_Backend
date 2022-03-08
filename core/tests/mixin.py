from usuario.models import Usuario
from usuario.tests import recipes

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import uuid

class APITestMixin:

    # Informações obrigatórias
    url = ''

    # Caso deseje alterar o nome, CPF, entre outros dados é
    # possível alterar esses atributos
    idUsuario = uuid.uuid4()
    nome = 'Nome para Teste'
    cpf = '03700076037'
    tipo = Usuario.PRODUTOR
    password = '12345678'
    telefone = '5599999999999'
    usuario_kwargs = {}


    def get_header_credencial(self):
        token = RefreshToken.for_user(self.user)
        return str(token)

    def get_client(self):
        client = APIClient()
        # client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial())
        return client

    def setUp(self):
        self.user = recipes.usuario.make(
            idUsuario=self.idUsuario, nome=self.nome, cpf=self.cpf, tipo=self.tipo,
            password=self.password, telefone=self.telefone, **self.usuario_kwargs
        )
        self.user.id = self.user.idUsuario
        self.client = self.get_client()
