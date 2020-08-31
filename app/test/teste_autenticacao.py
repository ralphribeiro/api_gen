import unittest
import json
from app.test.base import CasoDeTesteBase
from faker import Faker
import random

nome = ''
email = ''
chave = ''

def cria_usuario_teste():
    faker = Faker(['pt_PT', 'pt_BR', 'en_US'])
    Faker.seed(0)

    emails = []
    for i in range(10):
        emails.append(faker.email())

    return faker.name(), random.choice(emails), faker.swift()

def atualiza_globais():
    global nome
    global email
    global chave
    nome, email, chave = cria_usuario_teste()


def registra_usuario(obj):
    global nome
    global email
    global chave
    return obj.client.post(
        '/usuario/',
        data=json.dumps(dict(
            nome=nome,
            email=email,
            chave=chave
        )),
        content_type='application/json'
    )


def login_usuario(obj):
    return obj.client.post(
        '/autenticacao/login',
        data=json.dumps(dict(
            email=email,
            chave=chave
        )),
        content_type='application/json'
    )


class TesteAutenticacao(CasoDeTesteBase):
    def teste_1_usuario_registrado(self):
        with self.client:
            atualiza_globais()
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
            atualiza_globais()
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


    def teste_4_login_usuario_nao_registrado(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_usuario(self)
            dado = json.loads(response.data.decode())
            self.assertTrue(dado['status'] == 'falha')
            self.assertTrue(dado['message'] == 'Usuário ou/e Senha inválido(s).')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
      
if __name__ == '__main__':
    unittest.main()
