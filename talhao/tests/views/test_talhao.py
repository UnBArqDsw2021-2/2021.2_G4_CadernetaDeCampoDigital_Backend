from django.test import TestCase
from core.tests.mixin import APITestMixin
from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from propriedade.tests.recipes import propriedade

from talhao.models import Talhao
from talhao.tests.recipes import talhao


class TalhaoAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("talhao-create")

    def setUp(self):
        self.propriedade = propriedade.make()

    def _payload(self):
        return {
            "idPropriedade": self.propriedade.idPropriedade,
            "numero": 1
        }

    def test_cria_talhao(self):
        response = self.client.post(self.url, data=self._payload(), format="json")

        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Talhao.objects.count(), 1)

        talhao = Talhao.objects.first()
        self.assertEqual(talhao.idPropriedade, self.propriedade)
        self.assertEqual(talhao.numero, 1)

    @parameterized.expand(['idPropriedade', 'numero'])
    def test_nao_cria_talhao_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    def test_nao_cria_talhao_numero_repetido(self):
        payload = self._payload()
        talhao.make(idPropriedade=self.propriedade, numero=payload['numero'])

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Este número de talhão já existe nessa propriedade.',
            response.json()['non_field_errors']
        )

    def test_nao_cria_talhao_propriedade_inexistente(self):
        payload = self._payload()
        payload["idPropriedade"] = '00000000-0000-0000-0000-000000000000'

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'Pk inválido "{payload["idPropriedade"]}" - objeto não existe.',
            response.json()['idPropriedade']
        )

    def test_nao_cria_talhao_numero_negativo(self):
        payload = self._payload()
        payload['numero'] = -1

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Certifque-se de que este valor seja maior ou igual a 0.',
            response.json()['numero']
        )
