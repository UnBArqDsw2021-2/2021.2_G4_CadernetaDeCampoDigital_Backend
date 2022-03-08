from core.tests.mixin import APITestMixin

import datetime

from django.test import TestCase

from produtor.models.produtor import Produtor

from rest_framework.reverse import reverse_lazy


class ProdutorAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy('produtor-create')

    def setUp(self):
        pass

    def _payload(self):
        return {
            'usuario': {
                'cpf': '78299002052',
                'dataNascimento': datetime.date(2000, 1, 1),
                'telefone': '5561912345678',
                'nome': 'Jailson Mendes',
                'senha': 'senha_super_secreta'
            },
            'dap': 'c5Pnio21'
        }

    def test_cria_produtor(self):
        payload = self._payload()
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertIsNone(response.json.get('senha'))
        self.assertEqual(Produtor.objects.count(), 1)

        prod = Produtor.objects.first()
        self.assertEqual(prod.usuario.nome, payload['usuario']['nome'])
        self.assertEqual(prod.usuario.cpf, payload['usuario']['cpf'])
        self.assertEqual(prod.usuario.telefone, payload['usuario']['telefone'])
        self.assertNotEqual(prod.password, payload['usuario']['senha'])
        self.assertEqual(prod.dap, payload['dap'])
