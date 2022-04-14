from cultura.tests.recipes import cultura

from datetime import date, timedelta

from django.test import TestCase

from core.tests.mixin import APITestMixin
from core.consts.plantios import PLANTADO
from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from plantio.models import Plantio
from plantio.tests.recipes import plantio

from propriedade.tests.recipes import propriedade

from talhao.tests.recipes import talhao


class PlantioAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("plantio-create")

    def setUp(self):
        self.talhao = talhao.make()
        self.cultura = cultura.make()

    def _payload(self):
        return {
            'talhao': self.talhao.idTalhao,
            'cultura': self.cultura.idCultura,
            'dataPlantio': date.today(),
            'estado': PLANTADO
        }

    def test_cria_plantio(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Plantio.objects.count(), 1)

        plantio = Plantio.objects.first()
        self.assertEqual(plantio.cultura.idCultura, payload["cultura"])
        self.assertEqual(plantio.talhao.idTalhao, payload["talhao"])
        self.assertEqual(plantio.dataPlantio, payload["dataPlantio"])
        self.assertEqual(plantio.estado, payload["estado"])

    @parameterized.expand(['cultura', 'talhao', 'dataPlantio', 'estado'])
    def test_nao_cria_plantio_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('cultura', 'Cultura'), ('talhao', 'Talhao')])
    def test_nao_cria_plantio_objeto_inexistente(self, campo, msg):
        payload = self._payload()
        payload[campo] = '00000000-0000-0000-0000-000000000000'
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    def test_nao_cria_plantio_estado_inexistente(self):
        payload = self._payload()
        payload['estado'] = "inexistente"
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'''"{payload['estado']}" não é um escolha válido.''',
            response.json()['estado']
        )

    def test_nao_cria_plantio_data_no_futuro(self):
        payload = self._payload()
        payload['dataPlantio'] = date.today() + timedelta(days=1)
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Data de plantio no futuro.', response.json()['dataPlantio'])


class PlantioRetrieveUpdateAPIViewTest(APITestMixin, TestCase):

    def setUp(self):
        self.propriedade = propriedade.make()
        self.talhao = talhao.make(idPropriedade=self.propriedade)
        self.plantio = plantio.make(talhao=self.talhao)
        self.url = self.get_url()

    def _payload(self):
        return {
            'talhao': talhao.make(idPropriedade=self.propriedade).idTalhao,
            'cultura': cultura.make().idCultura,
            'dataPlantio': date.today(),
            'estado': PLANTADO
        }

    def get_url(self, idPlantio=None):
        if idPlantio is None:
            idPlantio = self.plantio.idPlantio
        return reverse_lazy("plantio-detail-update", kwargs={'pk': idPlantio})

    def test_detalha_plantio_existente(self):
        response = self.client.get(self.url, format="json")
        cultura_nome = response.json()['cultura']['nome']

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(5, len(response.json()))
        self.assertEqual(str(self.plantio.idPlantio), response.json()["idPlantio"])
        self.assertEqual(str(self.plantio.talhao.idTalhao), response.json()["talhao"])
        self.assertEqual(str(self.plantio.dataPlantio), response.json()["dataPlantio"])
        self.assertEqual(self.plantio.cultura.nome, cultura_nome)

    def test_nao_detalha_plantio_inexistente(self):
        url = self.get_url('00000000-0000-4000-8000-000000000000')

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])

    def test_atualiza_plantio(self):
        payload = self._payload()

        response = self.client.patch(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(Plantio.objects.count(), 1)

        self.plantio.refresh_from_db()
        self.assertEqual(self.plantio.cultura.idCultura, payload["cultura"])
        self.assertEqual(self.plantio.talhao.idTalhao, payload["talhao"])
        self.assertEqual(self.plantio.dataPlantio, payload["dataPlantio"])
        self.assertEqual(self.plantio.estado, payload["estado"])

    def test_nao_atualiza_plantio_inexistente(self):
        payload = self._payload()
        url = self.get_url('00000000-0000-4000-8000-000000000000')

        response = self.client.patch(url, data=payload, format="json")

        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])

    def test_nao_atualiza_plantio_talhao_nao_existe_na_propriedade_do_plantio(self):
        payload = self._payload()
        payload['talhao'] = talhao.make().idTalhao

        response = self.client.patch(self.url, data=payload, format="json")
        error_message = 'Esse talhão não pertence a propriedade onde está localizado esse plantio.'

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()['error'])

    @parameterized.expand(['cultura', 'talhao'])
    def test_nao_atualiza_plantio_cultura_talhao_inexistente(self, campo):
        payload = self._payload()
        payload[campo] = '00000000-0000-4000-8000-000000000000'

        response = self.client.patch(self.url, data=payload, format="json")
        error_message = f"Pk inválido \"{payload[campo]}\" - objeto não existe."

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()[campo])

    def test_nao_atualiza_plantio_data_futura(self):
        payload = self._payload()
        payload['dataPlantio'] = date.today() + timedelta(days=1)

        response = self.client.patch(self.url, data=payload, format="json")
        error_message = 'Data de plantio no futuro.'

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()['dataPlantio'])

    def test_nao_atualiza_estado_inexistente(self):
        payload = self._payload()
        payload['estado'] = 'Inexistente'

        response = self.client.patch(self.url, data=payload, format="json")
        error_message = f"\"{payload['estado']}\" não é um escolha válido."

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()['estado'])
