from django.test import TestCase

from core.tests.mixin import APITestMixin

from rest_framework.reverse import reverse_lazy

from agrotoxico.models import Agrotoxico, agrotoxico
from agrotoxico.models import Espera
from cultura.models import Cultura

from cultura.tests.recipes import cultura as c
from agrotoxico.tests.recipes import agrotoxico as a


class EsperaAPIViewTest(APITestMixin, TestCase):
    def test_cria_agrotoxico(self):
        agro = a.make()
        cul = c.make()
        e = Espera.objects.create(cultura=cul, agrotoxico=agro, diasCarencia=2)
        breakpoint()