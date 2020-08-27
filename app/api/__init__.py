from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_por_nome


db = SQLAlchemy()
flask_criptografia = Bcrypt()


def create_app(nome_config):
    app = Flask(__name__)
    app.config.from_object(config_por_nome[nome_config])
    db.init_app(app)
    flask_criptografia.init_app(app)

    return app
