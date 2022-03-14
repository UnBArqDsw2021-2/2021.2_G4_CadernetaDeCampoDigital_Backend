from django.test import TestCase
from core.tests.mixin import APITestMixin
from parameterized import parameterized

from produtor.models.produtor import Produtor
from produtor.tests.recipes import produtor

from rest_framework.reverse import reverse_lazy

from usuario.tests.views.usuario_base import UsuarioApiViewBase


class ProdutorAPIViewTest(UsuarioApiViewBase, APITestMixin, TestCase):
    url = reverse_lazy("produtor-create")

    def _payload(self):
        return {
            "usuario": super()._payload(),
            "dap": "ABC" + "9" * 22,
        }

    def test_cria_produtor(self):
        payload = self._payload()

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Produtor.objects.count(), 1)

        prod = Produtor.objects.first()
        self.assertEqual(prod.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(prod.usuario.cpf, payload["usuario"]["cpf"])
        self.assertEqual(prod.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(prod.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(prod.dap, payload["dap"])

    @parameterized.expand([
        ('', 'Este campo não pode ser em branco.'),
        ('invalido', 'DAP deve estar no formato: [A-Z]{3}[0-9]{22}.'),
    ])
    def test_nao_cria_produtor_dap_invalido(self, dap, msg):
        payload = self._payload()
        payload['dap'] = dap

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['dap'])

    def test_nao_cria_produtor_dap_duplicado(self):
        payload = self._payload()
        produtor.make(dap=payload["dap"])

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Esse campo deve ser  único.", response.json()["dap"])
