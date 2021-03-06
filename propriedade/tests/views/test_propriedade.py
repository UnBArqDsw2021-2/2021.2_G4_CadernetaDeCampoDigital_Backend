from core.consts.plantios import PLANTADO, FINALIZADO
from core.consts.usuarios import PRODUTOR, TECNICO

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
    url = reverse_lazy("propriedade-create-list")

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

        response = self.client.post(self.url, data=payload)
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

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('produtor', 'Produtor'), ('tecnico', 'Técnico')])
    def test_nao_cria_propriedade_usuario_inexistente(self, campo, msg):
        payload = self._payload()
        payload[campo] = "16175696077"

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(f'{msg} não existe.', response.json()[campo])

    def test_nao_cria_propriedade_estado_inexistente(self):
        payload = self._payload()
        payload['estado'] = "inexistente"

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'''"{payload['estado']}" não é um escolha válido.''',
            response.json()['estado']
        )

    def test_nao_cria_propriedade_numeroCasa_negativo(self):
        payload = self._payload()
        payload['numeroCasa'] = -1

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Certifque-se de que este valor seja maior ou igual a 0.',
            response.json()['numeroCasa']
        )

    def test_nao_cria_propriedade_hectares_negativo(self):
        payload = self._payload()
        payload['hectares'] = Decimal('-0.1')

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Certifque-se de que este valor seja maior ou igual a 0.01.',
            response.json()['hectares']
        )

    def test_nao_cria_propriedade_cep_invalido(self):
        payload = self._payload()
        payload['cep'] = "123456789"

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'CEP deve possuir 8 digítos numéricos.',
            response.json()['cep']
        )

    def test_lista_propriedade_de_um_produtor_autenticado(self):
        self.set_client_usuario(self.produtor.usuario)

        propriedade.make(produtor=self.produtor, tecnico=self.tecnico)
        propriedade.make(produtor=produtor.make(), tecnico=self.tecnico)

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(1, len(response.json()))

    def test_lista_propriedade_de_um_tecnico_autenticado(self):
        self.set_client_usuario(self.tecnico.usuario)

        propriedade.make(produtor=self.produtor, tecnico=self.tecnico)
        propriedade.make(produtor=self.produtor, tecnico=tecnico.make())

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(1, len(response.json()))


class PropriedadeSemTecnicoAPIViewTest(APITestMixin, TestCase):
    url = reverse_lazy("propriedade-list-sem-tecnico")

    def setUp(self):
        self.user.tipo = TECNICO
        self.user.save(update_fields=['tipo'])

        self.produtor = produtor.make(usuario__cpf='66326787009')
        self.tecnico = tecnico.make(usuario__cpf='42205106058')
        propriedade.make(tecnico=self.tecnico, _quantity=3)
        self.prop_sem_tecnico = []
        for prop in propriedade.make(tecnico=None, _quantity=3):
            self.prop_sem_tecnico.append(str(prop.idPropriedade))

    def test_lista_propriedades_sem_tecnico(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertTrue(set(self.prop_sem_tecnico).issubset(
            [prop["idPropriedade"] for prop in response.json()]
        ))

    def test_lista_vazio_propriedades_sem_tecnico(self):
        Propriedade.objects.filter(tecnico__isnull=True).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(response.json(), [])

    def test_lista_vazio_produtor_acessando(self):
        self.user.tipo = PRODUTOR
        self.user.save(update_fields=['tipo'])
        response = self.client.get(self.url)
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(response.json(), [])


class PropriedadeRetrieveUpdateAPIViewTest(APITestMixin, TestCase):

    def setUp(self):
        self.propriedade = propriedade.make()
        self.talhoes = talhao.make(idPropriedade=self.propriedade, _quantity=3)
        plantio.make(talhao=self.talhoes[0], estado=PLANTADO, _quantity=2)

        self.url = self.get_url()

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
        }

    def get_url(self, idPropriedade=None):
        if idPropriedade is None:
            idPropriedade = self.propriedade.idPropriedade
        return reverse_lazy("propriedade-detail-update", kwargs={'pk': idPropriedade})

    def test_detalha_propriedade_existente(self):
        response = self.client.get(self.url, format="json")
        qtd_talhao = len(response.json()['talhao'])
        qtd_plantio_primeiro_talhao = len(response.json()['talhao'][0]['plantio'])

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(12, len(response.json()))
        self.assertEqual(3, qtd_talhao)
        self.assertEqual(2, qtd_plantio_primeiro_talhao)
        self.assertEqual(str(self.propriedade.cep), response.json()["cep"])
        self.assertEqual(self.propriedade.estado, response.json()["estado"])
        self.assertEqual(self.propriedade.cidade, response.json()["cidade"])
        self.assertEqual(self.propriedade.bairro, response.json()["bairro"])
        self.assertEqual(self.propriedade.complemento, response.json()["complemento"])
        self.assertEqual(self.propriedade.numeroCasa, response.json()["numeroCasa"])
        self.assertEqual(self.propriedade.hectares, response.json()["hectares"])
        self.assertEqual(self.propriedade.logradouro, response.json()["logradouro"])

    def test_detalha_apenas_propriedade_encontrada(self):
        propriedade_diferente = propriedade.make()
        talhao.make(idPropriedade=propriedade_diferente, _quantity=10)

        response = self.client.get(self.url, format="json")
        qtd_talhao = len(response.json()['talhao'])

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(12, len(response.json()))
        self.assertEqual(3, qtd_talhao)

    def test_nao_detalha_plantios_nao_ativos(self):
        plantio.make(talhao=self.talhoes[0], estado=FINALIZADO, _quantity=5)

        response = self.client.get(self.url, format="json")
        qtd_plantio_primeiro_talhao = len(response.json()['talhao'][0]['plantio'])

        self.assertEqual(2, qtd_plantio_primeiro_talhao)

    def test_nao_detalha_propriedade_inexistente(self):
        url = self.get_url('00000000-0000-4000-8000-000000000000')

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])

    def test_atualiza_propriedade(self):
        payload = self._payload()
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(Propriedade.objects.count(), 1)

        self.propriedade.refresh_from_db()
        self.assertEqual(self.propriedade.cep, payload["cep"])
        self.assertEqual(self.propriedade.estado, payload["estado"])
        self.assertEqual(self.propriedade.cidade, payload["cidade"])
        self.assertEqual(self.propriedade.bairro, payload["bairro"])
        self.assertEqual(self.propriedade.complemento, payload["complemento"])
        self.assertEqual(self.propriedade.numeroCasa, payload["numeroCasa"])
        self.assertEqual(self.propriedade.hectares, payload["hectares"])
        self.assertEqual(self.propriedade.logradouro, payload["logradouro"])

    def test_nao_atualiza_propriedade_inexistente(self):
        payload = self._payload()
        url = self.get_url('00000000-0000-4000-8000-000000000000')
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])


class PropriedadeHistoricoPlantioAPIView(APITestMixin, TestCase):

    def setUp(self):
        self.propriedade = propriedade.make()
        self.url = self.get_url()
        self.talhoes = talhao.make(idPropriedade=self.propriedade, _quantity=3)
        talhao.make(idPropriedade=self.propriedade, _quantity=2)
        for t in self.talhoes:
            plantio.make(talhao=t)

    def get_url(self, idPropriedade=None):
        if idPropriedade is None:
            idPropriedade = self.propriedade.idPropriedade
        return reverse_lazy("propriedade-historico-plantio", kwargs={'idPropriedade': idPropriedade})

    def test_lista_plantios_do_talhao(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(len(response.json()), 3)

    def test_nao_lista_plantio_de_outra_propriedade(self):
        propriedade_diferente = propriedade.make()
        talhoes = talhao.make(idPropriedade=propriedade_diferente, _quantity=3)
        for t in talhoes:
            plantio.make(talhao=t)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(Plantio.objects.count(), 6)
        self.assertEqual(len(response.json()), 3)


class PropriedadeDeleteTecnicoAPIView(APITestMixin, TestCase):

    def setUp(self):
        self.produtor = produtor.make()
        self.tecnico = tecnico.make()
        self.propriedade = propriedade.make(tecnico=self.tecnico)
        self.url = self.get_url()

    def get_url(self, idPropriedade=None):
        if idPropriedade is None:
            idPropriedade = self.propriedade.idPropriedade
        return reverse_lazy("propriedade-delete-tecnico", kwargs={'idPropriedade': idPropriedade})

    def test_deleta_tecnico_propriedade(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial(self.tecnico.usuario))

        response = self.client.delete(self.url)
        data = Propriedade.objects.filter(idPropriedade=self.propriedade.idPropriedade).first()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(data.tecnico, None)
        self.assertEqual(self.propriedade.tecnico, self.tecnico)

    def test_nao_deleta_tecnico_propriedade_inexistente(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial(self.tecnico.usuario))
        url = self.get_url('00000000-0000-4000-8000-000000000000')

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado.', response.json()['detail'])

    def test_nao_deleta_outro_tecnico_propriedade(self):
        outro_tecnico = tecnico.make()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial(outro_tecnico.usuario))

        response = self.client.delete(self.url)
        error_message = 'Somente o técnico que está atribuido a propriedade pode se remover'

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()['error'])

    def test_produtor_nao_deleta_tecnico_propriedade(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_header_credencial(self.produtor.usuario))

        response = self.client.delete(self.url)
        error_message = 'Um produtor não pode remover técnico da propriedade'

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(error_message, response.json()['error'])
