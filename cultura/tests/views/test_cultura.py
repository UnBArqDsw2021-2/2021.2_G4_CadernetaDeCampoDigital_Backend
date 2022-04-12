
from core.tests.mixin import APIImageTestMixin

from rest_framework.reverse import reverse_lazy

from parameterized import parameterized

from cultura.models import Cultura
from cultura.tests.recipes import cultura as c


class CulturaAPIViewTest(APIImageTestMixin):
    url = reverse_lazy("cultura-create")

    def _payload(self):
        return {
            'nome': 'Cultura Muito Doida',
            'foto': self.get_image_file()
        }

    def test_cria_cultura(self):
        payload = self._payload()

        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Cultura.objects.count(), 1)

        cultura = Cultura.objects.first()
        self.assertEqual(cultura.nome, payload["nome"])
        self.assertNotEqual(cultura.foto.name, '')

    @parameterized.expand([
        ('nome', 'Este campo é obrigatório.'),
        ('foto', 'Nenhum arquivo foi submetido.')
    ])
    def test_nao_cria_cultura_atributos_obrigatorios(self, campo, mensage):
        payload = self._payload()
        del payload[campo]
        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(mensage, response.json()[campo])

    def test_nao_cria_cultura_nome_nao_unico(self):
        payload = self._payload()
        c.make(nome=payload['nome'])
        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Esse campo deve ser  único.', response.json()['nome'])
