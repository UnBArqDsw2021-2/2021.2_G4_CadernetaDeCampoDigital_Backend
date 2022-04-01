from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from agrotoxico.models import Espera

from cultura.tests.recipes import cultura as cultura_recipe
from agrotoxico.tests.recipes import agrotoxico as agrotoxico_recipe, espera as espera_recipe


class EsperaAPIViewTest(APITestMixin, TestCase):

    url = reverse_lazy('agrotoxico-espera-cultura')

    def setUp(self):
        self.cultura = cultura_recipe.make()
        self.agrotoxico = agrotoxico_recipe.make()

    def _payload(self):
        return {
            "agrotoxico": self.agrotoxico.idAgrotoxico,
            "cultura": self.cultura.idCultura,
            "diasCarencia": 1
        }

    def test_cria_espera(self):
        payload = self._payload()

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Espera.objects.count(), 1)

        espera = Espera.objects.first()
        self.assertEqual(espera.cultura.idCultura, payload["cultura"])
        self.assertEqual(espera.agrotoxico.idAgrotoxico, self.agrotoxico.idAgrotoxico)
        self.assertEqual(espera.diasCarencia, payload["diasCarencia"])

    @parameterized.expand(['cultura', 'diasCarencia'])
    def test_nao_cria_espera_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand(['cultura', 'agrotoxico'])
    def test_nao_cria_espera_objeto_inexistente(self, campo):
        payload = self._payload()
        payload[campo] = '00000000-0000-0000-0000-000000000000'

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    def test_nao_cria_espera_dias_carencia_negativo(self):
        payload = self._payload()
        payload["diasCarencia"] = -1

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            "Certifque-se de que este valor seja maior ou igual a 0.",
            response.json()["diasCarencia"]
        )

    def test_nao_cria_espera_cultura_repetida(self):
        payload = self._payload()
        espera_recipe.make(cultura=self.cultura, agrotoxico=self.agrotoxico)

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Os campos cultura, agrotoxico devem criar um set único.",
            response.json()["non_field_errors"][0]
        )
