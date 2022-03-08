import json
from urllib import response
from core.tests.mixin import APITestMixin

from django.test import TestCase

from produtor.models.produtor import Produtor
from produtor.tests.recipes import produtor

from rest_framework.reverse import reverse_lazy


class ProdutorAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("produtor-create")

    def _payload(self):
        return {
            "usuario": {
                "cpf": "78299002052",
                "dataNascimento": "2000-01-01",
                "telefone": "5561912345678",
                "nome": "Jailson Mendes",
                "senha": "senha_super_secreta",
            },
            "dap": "ABC"+"9"*22,
        }

    def _invalid_max_payload(self):
        return {
            "usuario": {
                "cpf": "12345678911",
                "dataNascimento": "11-05-2000",
                "telefone": "5561641115112345678",
                "nome": "a"*81,
                "senha": "b"*101,
            },
            "dap": "a"*26,
        }

    def _invalid_min_payload(self):
        return {
            "usuario": {
                "cpf": "1234567891",
                "dataNascimento": "11-05-2000",
                "telefone": "559999999999",
                "nome": "",
                "senha": "b"*7,
            },
            "dap": "",
        }

    def test_cria_produtor(self):
        payload = self._payload()

        response = self.client.post(self.url, payload, format="json")
        breakpoint()
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Produtor.objects.count(), 1)

        prod = Produtor.objects.first()
        self.assertEqual(prod.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(prod.usuario.cpf, payload["usuario"]["cpf"])
        self.assertEqual(prod.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(prod.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(prod.dap, payload["dap"])

    def test_cria_produtor_invalido_max(self):
        payload = self._invalid_max_payload()

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json().keys()), {'usuario', 'dap'})
        self.assertEqual(set(response.json()['usuario'].keys()), {'cpf', 'dataNascimento', 'nome', 'senha', 'telefone'})

    def test_cria_produtor_invalido_min(self):
        payload = self._invalid_min_payload()

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json().keys()), {'usuario', 'dap'})
        self.assertEqual(set(response.json()['usuario'].keys()), {'cpf', 'dataNascimento', 'nome', 'senha', 'telefone'})

    # FIXME: Os testes a partir daqui fazem parte do list
    # e deverão ser melhor tratados após a criação da API de list
    def test_list_produtores(self):
        produtor.make(_quantity=5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(len(response.json()), 5)
