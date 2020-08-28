import datetime
import jwt
from app.api.model.lista_negra import ListaNegraToken
from ..config import chave


from .. import db, flask_criptografia


class Usuario(db.Model):
    """Usuario Model para guardar detalhes relacionados a ele.
    """
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registrado_em = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    id_publico = db.Column(db.String(100), unique=True)
    nome = db.Column(db.String(50), unique=True)
    chave_hash = db.Column(db.String(100))

    @property
    def chave(self):
        raise AttributeError('chave: campo somente para escrita')

    @chave.setter
    def chave(self, chave):
        self.chave_hash = flask_criptografia.generate_password_hash(
            chave).decode('utf-8')

    def verifica_chave(self, chave):
        return flask_criptografia.check_password_hash(self.chave_hash, chave)

    def __repr__(self):
        return f'<Usuário "{self.nome}">'

    def codifica_token_autenticacao(self, usuario_id: str):
        """Gera tokens de autenticação

        Args:
            usuario_id (str):

        Returns:
            str:
        """
        try:
            carga = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': usuario_id
            }
            return jwt.encode(carga, chave, algorithm='HS256')
        except Exception as e:
            return str(e)

    @staticmethod
    def decodifica_token_autenticacao(token_autenticacao):
        """[summary]

        Args:
            token_autenticacao ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            payload = jwt.decode(token_autenticacao, chave)
            token_esta_bloqueado = ListaNegraToken.check_blacklist(token_autenticacao)
            if token_esta_bloqueado:
                return 'Token está na lista negra. Faça Login novamente.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Assinatura expidada. Faça Login novamente.'
        except jwt.InvalidTokenError:
            return 'Token inválido. Faça Login novamente.'
