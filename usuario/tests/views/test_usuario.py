from core.tests.mixin import APITestMixin

from django.test import TestCase

from parameterized import parameterized

from produtor.tests.recipes import produtor

from rest_framework.reverse import reverse_lazy

from tecnico.tests.recipes import tecnico

from usuario.models import Usuario


class UsuarioRetrieveUpdateAPIViewTest(APITestMixin, TestCase):

    def setUp(self):
        self.produtor = produtor.make()
        self.tecnico = tecnico.make()
        self.url_produtor = reverse_lazy(
            'usuario-details-update', kwargs={'idUsuario': self.produtor.usuario.idUsuario})
        self.url_tecnico = reverse_lazy(
            'usuario-details-update', kwargs={'idUsuario': self.tecnico.usuario.idUsuario})

    def _payload(self, kwargs={}):
        return {
            'usuario': {
                'cpf': '78299002052',
                'dataNascimento': '2000-01-01',
                'telefone': '5561912345678',
                'nome': 'Jailson Mendes',
                'senha': 'senha_super_secreta',
            },
            **kwargs
        }

    @parameterized.expand([('produtor',), ('tecnico',)])
    def test_atualiza_infos_gerais_do_usuario(self, tipo):
        payload = self._payload()

        response = self.client.patch(getattr(self, f'url_{tipo}'), payload, format='json')
        tipo_objeto = getattr(self, tipo)
        tipo_objeto.refresh_from_db()

        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(Usuario.objects.count(), 3)
        self.assertEqual(tipo_objeto.usuario.nome, payload['usuario']['nome'])
        self.assertEqual(tipo_objeto.usuario.cpf, payload['usuario']['cpf'])
        self.assertEqual(tipo_objeto.usuario.telefone, payload['usuario']['telefone'])
        self.assertNotEqual(tipo_objeto.usuario.password, payload['usuario']['senha'])

    @parameterized.expand([
        ('produtor', {'dap': 'ABC' + '9' * 22}),
        ('tecnico', {
            'crea': '1234567891',
            'formacao': 'Engenheiro Agronomo',
            'email': 'mendes.eduardo@email.com'
        })
    ])
    def test_atualiza_infos_especificas_do_usuario(self, tipo, campos):
        payload = self._payload(campos)
        response = self.client.patch(getattr(self, f'url_{tipo}'), payload, format='json')
        self.assertEqual(response.status_code, 200, response.json())
        tipo_objeto = getattr(self, tipo)
        tipo_objeto.refresh_from_db()

        for key, value in campos.items():
            with self.subTest(campo=key):
                self.assertEqual(getattr(tipo_objeto, key), value)

    def test_nao_atualiza_usuario_nao_encontrado(self):
        url = reverse_lazy(
            'usuario-details-update', kwargs={'idUsuario': '77bd5bff-ddb8-426b-80e7-0656a3da3741'})

        response = self.client.patch(url, self._payload(), format='json')
        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado', response.json()['detail'])

    @parameterized.expand([('produtor', ('dap',)), ('tecnico', ('crea', 'formacao', 'email'))])
    def test_detalha_infos_do_usuario(self, tipo, campos_proprios):
        produtor.make(_quantity=3)
        tecnico.make(_quantity=3)
        campos_comuns = ('nome', 'cpf', 'telefone', 'dataNascimento')
        response = self.client.get(getattr(self, f'url_{tipo}'))
        self.assertEqual(response.status_code, 200, response.json())

        for campo in campos_comuns:
            self.assertIsNotNone(response.json()['usuario'][campo])

        for campo in campos_proprios:
            self.assertIsNotNone(response.json()[campo])

    def test_nao_detalha_usuario_nao_encontrado(self):
        url = reverse_lazy(
            'usuario-details-update', kwargs={'idUsuario': '77bd5bff-ddb8-426b-80e7-0656a3da3741'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, response.json())
        self.assertIn('Não encontrado', response.json()['detail'])
