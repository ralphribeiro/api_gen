import unittest
import json
from app.test.base import CasoDeTesteBase
from faker import Faker


def cria_usuario_teste() -> dict:
    faker = Faker('pt_PT')
    Faker.seed(1000)
    return dict(
        nome=faker.name(),
        email=faker.email(),
        chave=faker.swift()
    )

def registra_usuario(obj):
    usu = cria_usuario_teste()
    return obj.client.post(
        '/usuario/',
        data=json.dumps(dict(
            nome=usu['nome'],
            email=usu['email'],
            chave=usu['chave']
        )),
        content_type='application/json'
    )


def login_usuario(obj):
    import pdb; pdb.set_trace()
    return obj.client.post(
        '/autenticacao/login',
        data=json.dumps(dict(
            email=obj['email'],
            chave=obj['chave']
        )),
        content_type='application/json'
    )


class TesteAutenticacao(CasoDeTesteBase):
    def teste_1_usuario_registrado(self):
        with self.client:
            response = registra_usuario(self)
            dado = json.loads(response.data.decode())
            self.assertTrue(dado['status'] == 'sucesso')
            self.assertTrue(dado['message'] == 'Registrado com sucesso.')
            self.assertTrue('Authorization' in dado)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def teste_2_se_registrado_com_usuario_registrado(self):
        with self.client:
            response = registra_usuario(self)
            dado = json.loads(response.data.decode())
            self.assertTrue(dado['status'] == 'falha')
            self.assertTrue(dado['message'] == 'Usuário existente. Faça o Login.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)
            

    def teste_3_login_usuario_registrado(self):
        with self.client:
            response = registra_usuario(self)
            dado_registro = json.loads(response.data.decode())
            self.assertTrue(dado_registro['status'] == 'sucesso')
            self.assertTrue(dado_registro['message'] == 'Registrado com sucesso.')
            self.assertTrue(dado_registro['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            response = login_usuario(self)
            dado_login = json.loads(response.data.decode())
            self.assertTrue(dado_login['status'] == 'sucesso')
            self.assertTrue(dado_login['message'] == 'Login feito com sucesso.')
            self.assertTrue(dado_login['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
      
if __name__ == '__main__':
    unittest.main()
