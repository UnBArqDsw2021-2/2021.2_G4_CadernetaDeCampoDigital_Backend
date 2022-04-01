from decimal import Decimal

from django.test import TestCase
from core.tests.mixin import APITestMixin
from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from plantio.models import Plantio
from plantio.tests.recipes import plantio

from propriedade.models import Propriedade
from propriedade.tests.recipes import propriedade

from produtor.tests.recipes import produtor

from tecnico.tests.recipes import tecnico

from talhao.tests.recipes import talhao


class PropriedadeAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("propriedade-create")

    def setUp(self):
        self.produtor = produtor.make(usuario__cpf='66326787009')
        self.tecnico = tecnico.make(usuario__cpf='42205106058')

    def _payload(self):
        return {
            "cep": "70256530",
            "estado": "DF",
            "cidade": "Brasília",
            "bairro": "Asa Sul",
            "complemento": "Conjunto Residencial 38",
            "numeroCasa": 12,
            "hectares": Decimal("6.5"),
            "logradouro": "Chácara do Amanhã",
            "produtor": self.produtor.usuario.cpf,
            "tecnico": self.tecnico.usuario.cpf
        }

    def test_cria_propriedade(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Propriedade.objects.count(), 1)

        propriedade = Propriedade.objects.first()
        self.assertEqual(propriedade.cep, payload["cep"])
        self.assertEqual(propriedade.estado, payload["estado"])
        self.assertEqual(propriedade.cidade, payload["cidade"])
        self.assertEqual(propriedade.bairro, payload["bairro"])
        self.assertEqual(propriedade.complemento, payload["complemento"])
        self.assertEqual(propriedade.numeroCasa, payload["numeroCasa"])
        self.assertEqual(propriedade.hectares, payload["hectares"])
        self.assertEqual(propriedade.logradouro, payload["logradouro"])
        self.assertEqual(propriedade.produtor.usuario.cpf, payload["produtor"])
        self.assertEqual(propriedade.tecnico.usuario.cpf, payload["tecnico"])

    @parameterized.expand([
        'cep', 'estado', 'cidade', 'bairro',
        'numeroCasa', 'logradouro', 'produtor'
    ])
    def test_nao_cria_propriedade_atributos_obrigatorios(self, campo):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('produtor', 'Produtor'), ('tecnico', 'Técnico')])
    def test_nao_cria_propriedade_usuario_inexistente(self, campo, msg):
        payload = self._payload()
        payload[campo] = "16175696077"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(f'{msg} não existe.', response.json()[campo])

    def test_nao_cria_propriedade_estado_inexistente(self):
        payload = self._payload()
        payload['estado'] = "inexistente"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'''"{payload['estado']}" não é um escolha válido.''',
            response.json()['estado']
        )

    def test_nao_cria_propriedade_numeroCasa_negativo(self):
        payload = self._payload()
        payload['numeroCasa'] = -1
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Certifque-se de que este valor seja maior ou igual a 0.',
            response.json()['numeroCasa']
        )

    def test_nao_cria_propriedade_hectares_negativo(self):
        payload = self._payload()
        payload['hectares'] = Decimal('-0.1')
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Certifque-se de que este valor seja maior ou igual a 0.01.',
            response.json()['hectares']
        )

    def test_nao_cria_propriedade_cep_invalido(self):
        payload = self._payload()
        payload['cep'] = "123456789"
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'CEP deve possuir 8 digítos numéricos.',
            response.json()['cep']
        )


class PropriedadeHistoricoPlantioAPIView(APITestMixin, TestCase):

    def setUp(self):
        self.propriedade = propriedade.make()
        self.url = reverse_lazy(
            "propriedade-historico-plantio", kwargs={'idPropriedade': self.propriedade.idPropriedade})
        self.talhoes = talhao.make(idPropriedade=self.propriedade, _quantity=3)
        talhao.make(idPropriedade=self.propriedade, _quantity=2)
        for t in self.talhoes:
            plantio.make(talhao=t)

    def test_lista_plantios_do_talhao(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(len(response.json()), 3)

    def test_nao_lista_plantio_de_outra_propriedade(self):
        url = reverse_lazy(
            "propriedade-historico-plantio", kwargs={'idPropriedade': self.propriedade.idPropriedade})
        propriedade_diferente = propriedade.make()
        talhoes = talhao.make(idPropriedade=propriedade_diferente, _quantity=3)
        for t in talhoes:
            plantio.make(talhao=t)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(Plantio.objects.count(), 6)
        self.assertEqual(len(response.json()), 3)
