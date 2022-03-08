from core.tests.mixin import APITestMixin

from django.test import TestCase

from produtor.models.produtor import Produtor

from rest_framework.reverse import reverse_lazy


class ProdutorAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("produtor-create")

    def _payload(self):
        return {
            "usuario": {
                "cpf": "78299002052",
                "dataNascimento": "2000-01-01",
                "telefone": "5561912345678",
                "nome": "Jailson Mendes",
                "senha": "senha_super_secreta",
            },
            "dap": "c5Pnio21",
        }

    def test_cria_produtor(self):
        payload = self._payload()

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.assertIsNone(response.json().get("senha"))
        self.assertEqual(Produtor.objects.count(), 1)

        prod = Produtor.objects.first()
        self.assertEqual(prod.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(prod.usuario.cpf, payload["usuario"]["cpf"])
        self.assertEqual(prod.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(prod.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(prod.dap, payload["dap"])
