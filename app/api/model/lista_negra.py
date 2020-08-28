from .. import db
import datetime


class ListaNegraToken(db.Model):
    """Token Model para armazenar os tokens JWT
    """
    __tablename__ = 'lista_negra_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    bloqueado_em = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.bloqueado_em = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<id: token: {self.token}>'

    @staticmethod
    def verifica_lista_negra(token_autenticado):
        res = ListaNegraToken.query.filter_by(token=str(token_autenticado)).first()
        if res:
            return True
        else:
            return False
