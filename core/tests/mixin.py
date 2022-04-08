import shutil
import tempfile
from io import BytesIO
from PIL import Image

from django.core.files.base import File
from django.test import override_settings, TestCase

from functools import partial

from core.consts.usuarios import PRODUTOR

from usuario.tests import recipes

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


MEDIA_ROOT = tempfile.mkdtemp()


class APITestMixin:

    # Informações obrigatórias
    url = ''

    # Caso deseje alterar o nome, CPF, entre outros dados é
    # possível alterar esses atributos
    nome = 'Nome para Teste'
    cpf = '03700076037'
    tipo = PRODUTOR
    password = '12345678'
    usuario_kwargs = {}

    def get_header_credencial(self, user=None):
        token = RefreshToken.for_user(self.user if not user else user)
        return str(token.access_token)

    def get_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial())
        client.post = partial(client.post, format='json')
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


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class APIImageTestMixin(APITestMixin, TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def get_image_file(self, name='test.png', ext='png', size=(1, 1), color=(255, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
