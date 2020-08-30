import unittest
import json
from app.test.base import CasoDeTesteBase
from faker import Faker

faker = Faker('pt_BR')
usuario_nome = faker.name()
usuario_email = faker.email()
chave = faker.cpf()


def registra_usuario(obj):
    return obj.client.post(
        '/usuario/',
        data=json.dumps(dict(
            nome=usuario_nome,
            email=usuario_email,
            chave=chave
        )),
        content_type='application/json'
    )


def login_usuario(obj):
    global usuario_nome
    global chave
    return obj.client.post(
        '/autenticacao/login',
        data=json.dumps(dict(
            email=usuario_email,
            chave=chave
        )),
        content_type='application/json'
    )


class TesteAutenticacao(CasoDeTesteBase):
    def teste_usuario_registrado(self):
        with self.client:
            response = registra_usuario(self)
            dado = json.loads(response.data.decode())
            self.assertTrue(dado['status'] == 'sucesso')
            self.assertTrue(dado['message'] == 'Registrado com sucesso.')
            self.assertTrue('Authorization' in dado)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def teste_se_registrado_com_usuario_registrado(self):
        with self.client:
            response = registra_usuario(self)
            dado = json.loads(response.data.decode())
            self.assertTrue(dado['status'] == 'falha')
            self.assertTrue(dado['message'] == 'Usuário existente. Faça o Login.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)
            
      
if __name__ == '__main__':
    unittest.main()
