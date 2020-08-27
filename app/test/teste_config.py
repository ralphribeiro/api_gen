import os
import unittest


from flask import current_app
from flask_testing import TestCase


from manage import app
from app.api.config import base_diretorio


class TesteConfigDesenvolvimento(TestCase):
    def create_app(self):
        app.config.from_object('app.api.config.ConfigDesenvolvimento')
        return app

    def teste_app_esta_em_modo_desenvolvimento(self):
        self.assertFalse(app.config['CHAVE_SECRETA'] is 'meu_precioso')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == f'sqlite:///{os.path.join(base_diretorio, "desenvolvimento.db")}'
        )


class TesteConfigTestes(TestCase):
    def create_app(self):
        app.config.from_object('app.api.config.ConfigTestes')
        return app

    def teste_app_esta_em_modo_de_testes(self):
        self.assertFalse(app.config['CHAVE_SECRETA'] is 'meu_precioso')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == f'sqlite:///{os.path.join(base_diretorio, "testes.db")}'
        )


class TesteConfigProducao(TestCase):
    def create_app(self):
        app.config.from_object('app.api.config.ConfigProducao')
        return app

    def teste_app_esta_em_modo_de_producao(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()

