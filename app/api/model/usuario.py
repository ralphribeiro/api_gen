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
        return f'<Pessoa "{self.nome}">'
