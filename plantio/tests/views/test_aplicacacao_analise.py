from core.tests.mixin import APITestMixin
from django.test import TestCase

from rest_framework.reverse import reverse_lazy

from plantio.tests import recipes


class AplicacaoAgrotoxicoAnaliseAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy('plantio-analise-aplicacao-agrotoxico')

    def test_list_aplicacao_produtor(self):
        recipes.aplicacao.make()
        aplicacoes = recipes.aplicacao.make(_quantity=2)
        produtor = aplicacoes[0].plantio.talhao.idPropriedade.produtor

        self.set_client_usuario(produtor.usuario)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_aplicacao_tecnico(self):
        recipes.aplicacao.make()
        aplicacoes = recipes.aplicacao.make(_quantity=2)
        tecnico = aplicacoes[0].plantio.talhao.idPropriedade.tecnico

        self.set_client_usuario(tecnico.usuario)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
