from django.test import TestCase
from core.tests.mixin import APITestMixin
from rest_framework.reverse import reverse_lazy
from parameterized import parameterized

from tecnico.models.tecnico import Tecnico
from tecnico.tests.recipes import tecnico as tecnico_recipe

from usuario.tests.views.usuario_base import UsuarioApiViewBase


class TecnicoAPIViewTest(UsuarioApiViewBase, APITestMixin, TestCase):
    url = reverse_lazy("tecnico-create")

    def _payload(self):
        return {
            "usuario": super()._payload(),
            "crea": "1234567891",
            "formacao": "Engenheiro Agronomo",
            "email": "mendes.eduardo@email.com",
        }

    def test_cria_tecnico(self):
        payload = self._payload()

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201, response.json())

        self.assertEqual(Tecnico.objects.count(), 1)

        tecnico = Tecnico.objects.first()
        self.assertEqual(tecnico.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(tecnico.usuario.cpf, payload["usuario"]["cpf"])
        self.assertEqual(tecnico.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(tecnico.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(tecnico.crea, payload["crea"])
        self.assertEqual(tecnico.formacao, payload["formacao"])
        self.assertEqual(tecnico.email, payload["email"])

    def test_nao_cria_tecnico_crea_duplicado(self):
        payload = self._payload()
        tecnico_recipe.make(crea=payload['crea'])

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Técnico já cadastrado.', response.json()['crea'])

    @parameterized.expand([
        '123456789',
        'ABC1234568',
        '12345678912',
    ])
    def test_nao_cria_tecnico_crea_invalido(self, crea):
        payload = self._payload()
        payload['crea'] = crea

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Crea deve possuir 10 digitos.', response.json()['crea'])
