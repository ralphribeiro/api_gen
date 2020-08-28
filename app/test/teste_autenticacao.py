import unittest
import json
from app.test.base import CasoDeTesteBase


def registra_usuario(self):
    return self.client.post(
        '/usuario/',
        data=json.dumps(dict(
            email='exemploum@um.com',
            nome='nomeexemploum',
            chave='654321'
        )),
        content_type='application/json'
    )


def login_usuario(self):
    return self.client.post(
        '/autenticacao/login',
        data=json.dumps(dict(
            email='exemploum@um.com',
            chave='654321'
        )),
        content_type='application/json'
    )


class TesteAutenticacao(CasoDeTesteBase):
    def test_login_usuario_logado(self):
        with self.client:
            usuario_response = registra_usuario(self)
            response_data = json.loads(usuario_response.data.decode())
            self.assertTrue(response_data['Autorizacao'])
            self.assertEqual(usuario_response.status_code, 201)

            login_response = login_usuario(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Autorizacao'])
            self.assertEqual(login_response.status_code, 200)

    def test_logout_valido(self):
        with self.client:
            usuario_response = registra_usuario(self)
            response_data = json.loads(usuario_response.data.decode())
            self.assertTrue(response_data['Autorizacao'])
            self.assertEqual(usuario_response.status_code, 201)

            login_response = login_usuario(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Autorizacao'])
            self.assertEqual(login_response.status_code, 200)

            response = self.client.post(
                '/autenticacao/logout',
                headers=dict(
                    Autorizacao='Bearer ' + json.loads(
                        login_response.data.decode()
                    )['Autorizacao']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
