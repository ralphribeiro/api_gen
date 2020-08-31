from app.api.config import chave
import unittest
import datetime
from faker import Faker


from app.api import db
from app.api.model.usuario import Usuario
from app.test.base import CasoDeTesteBase


class TesteUsuarioModel(CasoDeTesteBase):
    def __init__(self, methodName):
        self.setup()
        super().__init__(methodName)
    
    def setup(self):
        self.faker = Faker('pt_BR')

    def teste_codifica_token_autenticacao(self):
        usuario = Usuario(
            email=f'{str.lower(self.faker.email()+str(datetime.datetime.now().second))}',
            chave='test2',
            registrado_em=datetime.datetime.utcnow()
        )
        db.session.add(usuario)
        db.session.commit()
        token_autenticacao = usuario.codifica_token_autenticacao(usuario.id)
        self.assertTrue(isinstance(token_autenticacao, bytes))


    def teste_decodifica_token_autenticacao(self):
        usuario = Usuario(
            email=f'{str.lower(self.faker.email()+str(datetime.datetime.now().second))}',
            chave='test2',
            registrado_em=datetime.datetime.utcnow()
        )
        db.session.add(usuario)
        db.session.commit()
        token_autenticacao = usuario.codifica_token_autenticacao(usuario.id)
        self.assertTrue(isinstance(token_autenticacao, bytes))
        self.assertTrue(isinstance(Usuario.decodifica_token_autenticacao(token_autenticacao.decode("utf-8")), int))


if __name__ == '__main__':
    unittest.main()