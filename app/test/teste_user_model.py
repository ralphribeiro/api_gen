from app.api.config import chave
import unittest
import datetime


from app.api import db
from app.api.model.usuario import Usuario
from app.test.base import CasoDeTesteBase


class TesteUsuarioModel(CasoDeTesteBase):
    def teste_codifica_token_autenticacao(self):
        usuario = Usuario(
            email='test@test.com',
            chave='test',
            registrado_em=datetime.datetime.utcnow()
        )
        db.session.add(usuario)
        db.session.commit()
        token_autenticacao = usuario.codifica_token_autenticacao(usuario.id)
        self.assertTrue(isinstance(token_autenticacao, bytes))


    def teste_decodifica_token_autenticacao(self):
        usuario = Usuario(
            email='test@test.com',
            chave='test',
            registrado_em=datetime.datetime.utcnow()
        )
        db.session.add(usuario)
        db.session.commit()
        token_autenticacao = usuario.codifica_token_autenticacao(usuario.id)
        self.assertTrue(isinstance(token_autenticacao, bytes))
        self.assertTrue(Usuario.decodifica_token_autenticacao(token_autenticacao.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()