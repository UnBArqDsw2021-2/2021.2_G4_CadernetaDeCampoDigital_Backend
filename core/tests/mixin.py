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
    nome = 'Nome para Teste'
    cpf = '03700076037'
    tipo = Usuario.PRODUTOR
    password = '12345678'
    usuario_kwargs = {}


    def get_header_credencial(self):
        token = RefreshToken.for_user(self.user)
        return str(token.access_token)

    def get_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial())
        return client

    @classmethod
    def setUpClass(cls):
        # NOTE: Se o setUp não for na APITestMixin, executa ele primeiro e
        # após isso executa o específico da classe sendo executada
        if not isinstance(APITestMixin, cls) and cls.setUp is not APITestMixin.setUp:
            setUp_original = cls.setUp

            def setUpNovo(self, *args, **kwargs):
                APITestMixin.setUp(self)
                setUp_original(self, *args, **kwargs)

            cls.setUp = setUpNovo
        super().setUpClass()

    def setUp(self):
        self.user = recipes.usuario.make(
            nome=self.nome, cpf=self.cpf, tipo=self.tipo,
                password=self.password, **self.usuario_kwargs
        )
        self.user.id = self.user.idUsuario
        self.client = self.get_client()
