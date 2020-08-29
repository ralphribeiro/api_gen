import os
import unittest


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.api import create_app, db
from app.api.model import usuario, lista_negra



app = create_app('desenv')

app.register_blueprint(blueprint)

app.app_context().push()

gerente = Manager(app)

migrate = Migrate(app, db)

gerente.add_command('db', MigrateCommand)


@gerente.command
def run():
    app.run()


@gerente.command
def test():
    """
    Roda testes de unidade.
    """
    testes = unittest.TestLoader().discover('app/test', 'teste*.py')
    resultado = unittest.TextTestRunner(verbosity=2).run(testes)
    if resultado.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    gerente.run()
