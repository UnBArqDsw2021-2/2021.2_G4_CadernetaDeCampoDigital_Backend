from agrotoxico.tests.recipes import agrotoxico as a

from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from cultura.models import Cultura
from cultura.tests.recipes import cultura as c


class CulturaListCreateAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("cultura-list-create")

    def setUp(self):
        self.culturas = []
        for cultura in c.make(_quantity=10):
            self.culturas.append(str(cultura.idCultura))

    def _payload(self):
        return {
            'nome': 'Cultura Muito Doida'
        }

    def test_cria_cultura(self):
        Cultura.objects.all().delete()
        payload = self._payload()

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Cultura.objects.count(), 1)

        cultura = Cultura.objects.first()
        self.assertEqual(cultura.nome, payload["nome"])

    @parameterized.expand(['nome'])
    def test_nao_cria_cultura_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    def test_nao_cria_cultura_nome_nao_unico(self):
        payload = self._payload()
        c.make(nome=payload['nome'])
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Esse campo deve ser  único.', response.json()['nome'])

    def test_lista_culturas(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)
        self.assertTrue(set(self.culturas).issubset(
            [cult["idCultura"] for cult in response.json()]
        ))

    def test_list_vazio_culturas(self):
        Cultura.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(response.json(), [])

    def test_list_agrotoxicos_da_cultura(self):
        Cultura.objects.all().delete()
        cultura = c.make()
        cultura.agrotoxicos.add(a.make(), through_defaults={'diasCarencia': 10})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(len(response.json()[0]['agrotoxicos']), 1)
