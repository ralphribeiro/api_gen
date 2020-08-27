from app.api.config import chave
import uuid
import datetime


from app.api import db
from app.api.model.usuario import Usuario


def cria_um_novo_usuario(dado):
    usuario = Usuario.query.filter_by(email=dado['email']).first()
    if not usuario:
        usuario_novo = Usuario(
            id_publico=str(uuid.uuid4()),
            email=dado['email'],
            nome=dado['nome'],
            chave=dado['chave'],
            registrado_em=datetime.datetime.utcnow()
        )

        salva_alteracoes(usuario_novo)
        objeto_resposta = {
            'status': 'sucesso',
            'mensagem': 'Registrado com sucesso.'
        }
        return objeto_resposta, 201
    
    else:
        objeto_resposta = {
            'status': 'sucesso',
            'mensagem': 'Usuário existente. Faça o Login.s'
        }
        return objeto_resposta, 409


def obtem_usuarios():
    return Usuario.query.all()


def obtem_usuario(id_publico):
    return Usuario.query.filter_by(id_publico=id_publico).first()


def salva_alteracoes(dado):
    db.session.add(dado)
    db.session.commit()
