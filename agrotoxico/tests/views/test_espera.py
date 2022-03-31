from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from agrotoxico.models import Espera

from cultura.tests.recipes import cultura as c
from agrotoxico.tests.recipes import agrotoxico as a


class EsperaAPIViewTest(APITestMixin, TestCase):

    def url(self, idAgrotoxico=None):
        if idAgrotoxico is None:
            idAgrotoxico = self.agrotoxico.idAgrotoxico
        return reverse_lazy('agrotoxico-espera-cultura', args=[idAgrotoxico])

    def setUp(self):
        self.cultura = c.make()
        self.agrotoxico = a.make()

    def _payload(self):
        return {
            "cultura": self.cultura.idCultura,
            "diasCarencia": 1
        }

    def test_cria_agrotoxico(self):
        payload = self._payload()

        response = self.client.post(self.url(), data=payload, format='json')

        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Espera.objects.count(), 1)

        espera = Espera.objects.first()
        self.assertEqual(espera.cultura.idCultura, payload["cultura"])
        self.assertEqual(espera.agrotoxico.idAgrotoxico, self.agrotoxico.idAgrotoxico)
        self.assertEqual(espera.diasCarencia, payload["diasCarencia"])
