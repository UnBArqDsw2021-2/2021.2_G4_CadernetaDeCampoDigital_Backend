from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from agrotoxico.models import TipoAgrotoxico
from agrotoxico.tests.recipes import tipo_agrotoxico as tipo_agrotoxico_recipe


class TipoAgrotoxicoListCreateAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("tipo-agrotoxico-list-create")

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
        tipo_agrotoxico_recipe.make(nome=payload['nome'])

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Esse campo deve ser  único.', response.json()['nome'])

    @parameterized.expand([
        ("", "Este campo não pode ser em branco."),
        ("a"*81, "Certifique-se de que este campo não tenha mais de 80 caracteres.")
    ])
    def test_nao_cria_agrotoxico_nome_invalido(self, nome, msg):
        payload = self._payload()
        payload['nome'] = nome

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()["nome"])

    def test_lista_agrotoxico(self):
        tipo_agrotoxico_recipe.make(_quantity=10)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.json()))

    def test_lista_agrotoxico_estrutura(self):
        tipo_agrotoxico = tipo_agrotoxico_recipe.make()

        response = self.client.get(self.url)
        data = response.json()[0]

        self.assertEqual(str(tipo_agrotoxico.idTipoAgrotoxico), data["idTipoAgrotoxico"])
        self.assertEqual(tipo_agrotoxico.nome, data["nome"])
