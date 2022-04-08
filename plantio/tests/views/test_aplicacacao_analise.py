from datetime import date
from decimal import Decimal
from parameterized import parameterized

from django.test import TestCase
from core.tests.mixin import APITestMixin, APIImageTestMixin

from rest_framework.reverse import reverse_lazy
from plantio.models.aplicacao import AplicacaoAgrotoxico

from plantio.tests import recipes
from agrotoxico.tests.recipes import agrotoxico as agrotoxico_recipe
from tecnico.tests.recipes import tecnico as tecnico_recipe
from produtor.tests.recipes import produtor as produtor_recipe


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


class AplicacaoAgrotoxicoAnaliseUpdateAPIViewTest(APIImageTestMixin):

    def setUp(self):
        self.aplicacao = recipes.aplicacao.make()
        self.produtor = self.aplicacao.propriedade.produtor
        self.agrotoxico = agrotoxico_recipe.make()
        self.tecnico = tecnico_recipe.make()
        self.aplicacao.propriedade.tecnico = self.tecnico
        self.aplicacao.propriedade.save()

    def get_url(self, idAplicacao=None):
        if idAplicacao is None:
            idAplicacao = self.aplicacao.idAplicacao

        return reverse_lazy('plantio-analise-aplicacao-agrotoxico-update', kwargs={"idAplicacao": idAplicacao})

    def _payload(self):
        return {
            'agrotoxico': self.agrotoxico.idAgrotoxico,
            'dataAplicacao': date.today(),
            'dosagemAplicacao': Decimal('0.42'),
            'fotoAgrotoxico': self.get_image_file()
        }

    def test_tecnico_atualiza_aplicacao(self):
        payload = self._payload()

        self.set_client_usuario(self.tecnico.usuario)

        response = self.client.patch(self.get_url(), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        self.aplicacao.refresh_from_db()

        self.assertNotEqual(self.aplicacao.fotoAgrotoxico.name, '')
        self.assertEqual(self.aplicacao.dosagemAplicacao, payload["dosagemAplicacao"])
        self.assertEqual(self.aplicacao.dataAplicacao, payload["dataAplicacao"])
        self.assertEqual(self.aplicacao.agrotoxico.idAgrotoxico, payload["agrotoxico"])

    @parameterized.expand(['idAplicacao', 'plantio'])
    def test_tecnico_nao_atualiza_aplicacao_campos_leitura(self, campo, campo_alt=None):
        payload = self._payload()
        payload[campo] = "1231"

        self.set_client_usuario(self.tecnico.usuario)

        response = self.client.patch(self.get_url(), payload)

        self.assertEqual(response.status_code, 200)

        aplicacao = response.json()
        self.aplicacao.refresh_from_db()

        self.assertIsNotNone(getattr(self.aplicacao, campo))
        self.assertIsNotNone(aplicacao.get(campo))

    def test_tecnico_nao_atualiza_aplicacao_campo_produtor(self):
        payload = self._payload()
        payload["produtor"] = produtor_recipe.make()

        self.set_client_usuario(self.tecnico.usuario)

        response = self.client.patch(self.get_url(), payload)

        self.assertEqual(response.status_code, 200)

        self.aplicacao.refresh_from_db()

        self.assertNotEqual(self.aplicacao.propriedade.produtor, payload["produtor"])

    def test_produtor_nao_atualiza_aplicacao(self):
        payload = self._payload()

        self.set_client_usuario(self.produtor.usuario)

        response = self.client.patch(self.get_url(), payload)

        self.assertEqual(response.status_code, 403)
