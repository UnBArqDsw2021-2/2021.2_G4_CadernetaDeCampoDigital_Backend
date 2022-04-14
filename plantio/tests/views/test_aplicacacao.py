from agrotoxico.tests.recipes import agrotoxico as a

from datetime import date, timedelta

from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile

from core.tests.mixin import APIImageTestMixin
from core.consts.agrotoxicos import AplicacaoEstados

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from plantio.models import AplicacaoAgrotoxico
from plantio.tests import recipes


class AplicacaoAgrotoxicoAPIViewTest(APIImageTestMixin):
    url = reverse_lazy('plantio-associar')

    def setUp(self):
        self.plantio = recipes.plantio.make()
        self.agrotoxico = a.make()

    def _payload_agrotoxico(self):
        return {
            'plantio': self.plantio.idPlantio,
            'agrotoxico': self.agrotoxico.idAgrotoxico,
            'dataAplicacao': date.today(),
            'dosagemAplicacao': Decimal('0.42'),
        }

    def _payload_fotoAgrotoxico(self):
        payload = self._payload_agrotoxico()

        payload["fotoAgrotoxico"] = self.get_image_file()

        del payload["agrotoxico"]
        return payload

    def test_cria_aplicacao_com_agrotoxico(self):
        payload = self._payload_agrotoxico()

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        associacao = AplicacaoAgrotoxico.objects.first()
        self.assertEqual(associacao.plantio, self.plantio)
        self.assertEqual(associacao.agrotoxico, self.agrotoxico)
        self.assertEqual(associacao.dataAplicacao, payload['dataAplicacao'])
        self.assertEqual(associacao.fotoAgrotoxico.name, '')
        self.assertEqual(associacao.dosagemAplicacao, payload['dosagemAplicacao'])
        self.assertEqual(associacao.estadoAnalise, AplicacaoEstados.SUCESSO)

    def test_cria_aplicacao_com_fotoAgrotoxico(self):
        payload = self._payload_fotoAgrotoxico()

        response = self.client.post(self.url, payload, format='multipart')
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        associacao = AplicacaoAgrotoxico.objects.first()
        self.assertEqual(associacao.plantio, self.plantio)
        self.assertEqual(associacao.dataAplicacao, payload['dataAplicacao'])
        self.assertIsNone(associacao.agrotoxico)
        self.assertNotEqual(associacao.fotoAgrotoxico.name, '')
        self.assertEqual(associacao.dosagemAplicacao, payload['dosagemAplicacao'])
        self.assertEqual(associacao.estadoAnalise, AplicacaoEstados.ANALISE)

    def test_cria_aplicacao_agrotoxico_sem_dosagemAplicacao(self):
        payload = self._payload_agrotoxico()
        del payload['dosagemAplicacao']

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(AplicacaoAgrotoxico.objects.count(), 1)

        associacao = AplicacaoAgrotoxico.objects.first()
        self.assertEqual(associacao.plantio, self.plantio)
        self.assertEqual(associacao.dataAplicacao, payload['dataAplicacao'])
        self.assertIsNone(associacao.dosagemAplicacao)
        self.assertEqual(associacao.estadoAnalise, AplicacaoEstados.SUCESSO)

    @parameterized.expand(['plantio', 'dataAplicacao'])
    def test_nao_cria_aplicacao_atributos_obrigatorios(self, campo):
        payload = self._payload_agrotoxico()
        del payload[campo]
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('Este campo é obrigatório.', response.json()[campo])

    @parameterized.expand([('plantio', 'Plantio'), ('agrotoxico', 'Agrotoxico')])
    def test_nao_cria_aplicacao_objeto_inexistente(self, campo, msg):
        payload = self._payload_agrotoxico()
        payload[campo] = '00000000-0000-0000-0000-000000000000'
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f"Pk inválido \"{payload[campo]}\" - objeto não existe.",
            response.json()[campo]
        )

    def test_nao_cria_aplicacao_ja_existente(self):
        payload = self._payload_agrotoxico()
        recipes.aplicacao.make(
            plantio=self.plantio, agrotoxico=self.agrotoxico,
            dataAplicacao=payload['dataAplicacao'], dosagemAplicacao=payload['dosagemAplicacao']
        )
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            f'Esse agrotóxico já foi aplicado nessa plantação na data {payload["dataAplicacao"]}.',
            response.json()['non_field_errors'][0]
        )

    def test_nao_cria_aplicacao_data_no_futuro(self):
        payload = self._payload_agrotoxico()
        payload['dataAplicacao'] += timedelta(days=1)
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Data de aplicação no futuro.', response.json()['dataAplicacao'])

    def test_nao_cria_aplicao_sem_agrotoxico_e_fotoAgrotoxico(self):
        payload = self._payload_agrotoxico()
        del payload["agrotoxico"]

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "É necessário enviar ou o agrotóxico ou a foto do agrotóxico.",
            response.json()["non_field_errors"]
        )

    def test_nao_cria_aplicao_com_agrotoxico_e_fotoAgrotoxico(self):
        payload = self._payload_fotoAgrotoxico()
        payload["agrotoxico"] = self.agrotoxico.idAgrotoxico

        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "É necessário enviar ou o agrotóxico ou a foto do agrotóxico.",
            response.json()["non_field_errors"]
        )

    def test_nao_cria_aplicacao_fotoAgrotoxico_invalida(self):
        payload = self._payload_fotoAgrotoxico()
        payload["fotoAgrotoxico"] = SimpleUploadedFile('foto.png', b'0000', content_type="image/png")

        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Fazer upload de uma imagem válida. O arquivo enviado não é um arquivo de imagem ou está corrompido.",
            response.json()["fotoAgrotoxico"]
        )
