from core.tests.mixin import APITestMixin
from django.test import TestCase

from rest_framework.reverse import reverse_lazy

from tecnico.models.tecnico import Tecnico

from tecnico.tests.recipes import tecnico as tecnico_recipe

class TecnicoAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("tecnico-create")

    def _payload(self):
        return {
            "usuario": {
                "cpf": "75610670039",
                "dataNascimento": "2000-01-01",
                "telefone": "5561912345678",
                "nome": "Mendes Eduardo",
                "senha": "senha_super_secreta",
            },
            "crea": "ABC123456",
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

    def test_cria_tecnico_crea_duplicado(self):
        payload = self._payload()
        tecnico_recipe.make(crea=payload['crea'])
        
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('tecnico com este crea já existe.', response.json()['crea'])
