from parameterized import parameterized

from usuario.models import usuario
from usuario.tests.recipes import usuario as usuario_recipe


class UsuarioApiViewBase:
    url = ""

    def _payload(self):
        return {
            "cpf": "78299002052",
            "dataNascimento": "2000-01-01",
            "telefone": "5561912345678",
            "nome": "Jailson Mendes",
            "senha": "senha_super_secreta",
        }

    @parameterized.expand(
        [
            ('', 'Este campo não pode ser em branco.'),
            ('123456789', 'CPF deve conter 11 dígitos.'),
            ('11111111111', 'CPF deve conter 11 dígitos.'),
            ('11111111181', 'CPF inválido.'),
            ('11111111118', 'CPF inválido.'),
        ]
    )
    def test_nao_cria_usuario_cpf_invalido(self, cpf, msg):
        payload = self._payload()
        payload['usuario']['cpf'] = cpf

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['usuario']['cpf'])

    def test_nao_cria_usuario_data_formato_invalido(self):
        payload = self._payload()
        payload['usuario']['dataNascimento'] = '11-05-2000'

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.',
            response.json()['usuario']['dataNascimento'],
        )

    @parameterized.expand([('5561641115112345678',), ('559999999999',), ('invalido',)])
    def test_nao_cria_usuario_telefone_invalido(self, telefone):
        payload = self._payload()
        payload['usuario']['telefone'] = telefone

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Este número de telefone não é válido.',
            response.json()['usuario']['telefone'],
        )

    @parameterized.expand(
        [
            (
                'a' * 101,
                'Certifique-se de que este campo não tenha mais de 100 caracteres.',
            ),
            ('b' * 7, 'Certifique-se de que este campo tenha mais de 8 caracteres.'),
        ]
    )
    def test_nao_cria_usuario_senha_invalida(self, senha, msg):
        payload = self._payload()
        payload['usuario']['senha'] = senha

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['usuario']['senha'])

    def test_nao_cria_produtor_cpf_duplicado(self):
        payload = self._payload()
        usuario_recipe.make(cpf=payload['usuario']['cpf'])

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Esse campo deve ser  único.", response.json()["usuario"]["cpf"])
