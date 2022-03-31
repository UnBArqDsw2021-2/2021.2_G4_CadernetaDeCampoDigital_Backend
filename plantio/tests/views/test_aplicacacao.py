from agrotoxico.tests.recipes import agrotoxico as a

from datetime import date, timedelta

from decimal import Decimal

from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from plantio.models import AplicacaoAgrotoxico
from plantio.tests import recipes


class AplicacaoAgrotoxicoAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy('plantio-associar')

    def setUp(self):
        self.plantio = recipes.plantio.make()
        self.agrotoxico = a.make()

    def _payload(self):
        return {
            'plantio': self.plantio.idPlantio,
            'agrotoxico': self.agrotoxico.idAgrotoxico,
            'dataAplicacao': date.today(),
            # 'fotoAgrotoxico': ,
            'dosagemAplicacao': Decimal('0.42'),
        }

    def test_cria_aplicacao_agrotoxico(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        associacao = AplicacaoAgrotoxico.objects.first()
        self.assertEqual(associacao.plantio, self.plantio)
        self.assertEqual(associacao.agrotoxico, self.agrotoxico)
        self.assertEqual(associacao.dataAplicacao, payload['dataAplicacao'])
        # self.assertIsNone(associacao.caminhoFotoAgrotoxico)
        self.assertEqual(associacao.dosagemAplicacao, payload['dosagemAplicacao'])
        self.assertEqual(associacao.estadoAnalise, 'A')

    def test_cria_aplicacao_agrotoxico_sem_atributos_opcionais(self):
        payload = self._payload()
        # for campo in ('agrotoxico', 'fotoAgrotoxico', 'dosagemAplicacao'):
        for campo in ('agrotoxico', 'dosagemAplicacao'):
            del payload[campo]

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        associacao = AplicacaoAgrotoxico.objects.first()
        self.assertEqual(associacao.plantio, self.plantio)
        self.assertIsNone(associacao.agrotoxico)
        self.assertEqual(associacao.dataAplicacao, payload['dataAplicacao'])
        # self.assertIsNone(associacao.caminhoFotoAgrotoxico)
        self.assertIsNone(associacao.dosagemAplicacao)
        self.assertEqual(associacao.estadoAnalise, 'A')

    @parameterized.expand(['plantio', 'dataAplicacao'])
    def test_nao_cria_aplicacao_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('plantio', 'Plantio'), ('agrotoxico', 'Agrotoxico')])
    def test_nao_cria_aplicacao_objeto_inexistente(self, campo, msg):
        payload = self._payload()
        payload[campo] = '00000000-0000-0000-0000-000000000000'
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    def test_nao_cria_aplicacao_ja_existente(self):
        payload = self._payload()
        recipes.aplicacao.make(
            plantio=self.plantio, agrotoxico=self.agrotoxico,
            dataAplicacao=payload['dataAplicacao'], dosagemAplicacao=payload['dosagemAplicacao']
        )
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'Esse agrotóxico já foi aplicado nessa plantação na data {payload["dataAplicacao"]}.',
            response.json()['non_field_errors'][0]
        )

    def test_nao_cria_aplicacao_data_no_futuro(self):
        payload = self._payload()
        payload['dataAplicacao'] += timedelta(days=1)
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Data de aplicação no futuro.', response.json()['dataAplicacao'])
