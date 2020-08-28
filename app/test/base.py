from flask_testing import TestCase
from app.api import db
from manage import app


class CasoDeTesteBase(TestCase):
    """Base de testes
    """

    def create_app(self):
        app.config.from_object('app.api.config.ConfigTestes')
        return app

    def setup(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        