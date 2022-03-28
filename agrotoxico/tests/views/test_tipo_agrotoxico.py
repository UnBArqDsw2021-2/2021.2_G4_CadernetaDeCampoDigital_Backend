from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from agrotoxico.models import TipoAgrotoxico
from agrotoxico.tests.recipes import tipo_agrotoxico as ta


class TipoAgrotoxicoAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("tipo-agrotoxico-create")

    def _payload(self):
        return {
            'nome': 'Inseticida'
        }

    def test_cria_tipo_agrotoxico(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(TipoAgrotoxico.objects.count(), 1)

        tipo_agrotoxico = TipoAgrotoxico.objects.first()
        self.assertEqual(tipo_agrotoxico.nome, payload["nome"])

    @parameterized.expand(['nome'])
    def test_nao_cria_tipo_agrotoxico_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    def test_nao_cria_tipo_agrotoxico_nome_nao_unico(self):
        payload = self._payload()
        ta.make(nome=payload['nome'])

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Esse campo deve ser  único.', response.json()['nome'])
