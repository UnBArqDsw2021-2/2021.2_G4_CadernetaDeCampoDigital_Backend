from datetime import date, timedelta

from decimal import Decimal

from django.test import TestCase

from core.tests.mixin import APITestMixin
from core.consts.estados import UF_CHOICES

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from plantio.models import Plantio

from talhao.tests.recipes import talhao


class PlantioAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("plantio-create")

    def setUp(self):
        self.talhao = talhao.make()

    def _payload(self):
        return {
            'talhao': self.talhao.idTalhao,
            # 'cultura': self.cultura.idCultura,
            'dataPlantio': date.today(),
            'estado': UF_CHOICES[7][0]
        }

    def test_cria_plantio(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Plantio.objects.count(), 1)

        plantio = Plantio.objects.first()
        # self.assertEqual(plantio.cultura.idCultura, payload["cultura"])
        self.assertEqual(plantio.talhao.idTalhao, payload["talhao"])
        self.assertEqual(plantio.dataPlantio, payload["dataPlantio"])
        self.assertEqual(plantio.estado, payload["estado"])

    # @parameterized.expand(['cultura', 'talhao', 'dataPlantio', 'estado'])
    @parameterized.expand(['talhao', 'dataPlantio', 'estado'])
    def test_nao_cria_plantio_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    # @parameterized.expand([('cultura', 'Cultura'), ('talhao', 'Talhao')])
    @parameterized.expand([('talhao', 'Talhao')])
    def test_nao_cria_plantio_objeto_inexistente(self, campo, msg):
        payload = self._payload()
        payload[campo] = '00000000-0000-0000-0000-000000000000'
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    def test_nao_cria_plantio_estado_inexistente(self):
        payload = self._payload()
        payload['estado'] = "inexistente"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'''"{payload['estado']}" não é um escolha válido.''',
            response.json()['estado']
        )

    def test_nao_cria_plantio_data_no_futuro(self):
        payload = self._payload()
        payload['dataPlantio'] = date.today() + timedelta(days=1)
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Data de plantio no futuro.', response.json()['dataPlantio'])
