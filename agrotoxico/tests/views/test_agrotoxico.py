from django.test import TestCase

from core.tests.mixin import APITestMixin

from cultura.tests.recipes import espera

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from agrotoxico.models import Agrotoxico
from agrotoxico.tests.recipes import tipo_agrotoxico as tipo_agrotoxico_recipe, agrotoxico as agrotoxico_recipe

from plantio.tests.recipes import aplicacao


class AgrotoxicoListCreateAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("agrotoxico-list-create")

    def setUp(self):
        self.tipo_agrotoxico = tipo_agrotoxico_recipe.make()

    def _payload(self):
        return {
            'nome': 'Mata Muriçoca',
            'tipo': self.tipo_agrotoxico.idTipoAgrotoxico
        }

    def test_cria_agrotoxico(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Agrotoxico.objects.count(), 1)

        tipo_agrotoxico = Agrotoxico.objects.first()
        self.assertEqual(tipo_agrotoxico.nome, payload["nome"])
        self.assertEqual(tipo_agrotoxico.tipo.idTipoAgrotoxico, payload["tipo"])

    @parameterized.expand(['nome', 'tipo'])
    def test_nao_cria_agrotoxico_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('tipo')])
    def test_nao_cria_agrotoxico_objeto_inexistente(self, campo):
        payload = self._payload()
        payload[campo] = '00000000-0000-0000-0000-000000000000'

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    @parameterized.expand([
        ("", "Este campo não pode ser em branco."),
        ("a"*81, "Certifique-se de que este campo não tenha mais de 80 caracteres.")
    ])
    def test_nao_cria_agrotoxico_nome_invalido(self, nome, msg):
        payload = self._payload()
        payload['nome'] = nome

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()["nome"])

    def test_lista_agrotoxico(self):
        agrotoxico_recipe.make(_quantity=10)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.json()))

    def test_lista_agrotoxico_estrutura(self):
        agrotoxico = agrotoxico_recipe.make()
        tipo_agrotoxico = agrotoxico.tipo

        response = self.client.get(self.url)
        data = response.json()[0]

        self.assertEqual(str(agrotoxico.idAgrotoxico), data["idAgrotoxico"])
        self.assertEqual(agrotoxico.nome, data["nome"])
        self.assertEqual(str(tipo_agrotoxico.idTipoAgrotoxico), data["tipo"]["idTipoAgrotoxico"])
        self.assertEqual(tipo_agrotoxico.nome, data["tipo"]["nome"])


class AgrotoxicoDestroyAPIViewTest(APITestMixin, TestCase):

    def setUp(self):
        self.agrotoxico = agrotoxico_recipe.make()
        self.url = self.get_url()

    def get_url(self, idAgrotoxico=None):
        if idAgrotoxico is None:
            idAgrotoxico = self.agrotoxico.idAgrotoxico
        return reverse_lazy("agrotoxico-destroy", kwargs={'pk': idAgrotoxico})

    def test_deleta_agrotoxico(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Agrotoxico.objects.count(), 0)

    def test_nao_deleta_agrotoxico_inexistente(self):
        url = self.get_url('00000000-0000-4000-8000-000000000000')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])

    def test_nao_deleta_agrotoxico_sendo_aplicado(self):
        aplicacao.make(agrotoxico=self.agrotoxico)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Não é possível apagar um agrotoxico que já foi aplicado em um plantio.',
            response.json()['agrotoxico']
        )
        self.assertEqual(Agrotoxico.objects.count(), 1)

    def test_nao_deleta_agrotoxico_sendo_esperado(self):
        espera.make(agrotoxico=self.agrotoxico)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Não é possível apagar um agrotoxico que está em tempo de espera de uma cultura.',
            response.json()['agrotoxico']
        )
        self.assertEqual(Agrotoxico.objects.count(), 1)
