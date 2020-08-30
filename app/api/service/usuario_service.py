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
        return gera_token(usuario_novo)
    else:
        objeto_resposta = {
            'status': 'falha',
            'message': 'Usuário existente. Faça o Login.'
        }
        return objeto_resposta, 409


def obtem_usuarios():
    return Usuario.query.all()


def obtem_usuario(id_publico):
    return Usuario.query.filter_by(id_publico=id_publico).first()


def salva_alteracoes(dado):
    db.session.add(dado)
    db.session.commit()


def gera_token(usuario):
    try:
        token_autenticacao = usuario.codifica_token_autenticacao(usuario.id)
        objeto_resposta = {
            'status': 'sucesso',
            'message': 'Registrado com sucesso.',
            'Authorization': token_autenticacao.decode()
        }
        return objeto_resposta, 201
    except Exception as e:
        objeto_resposta = {
            'status': 'falha',
            'message': 'Ocorreu um erro inesperado, tente novamente mais tarde'
        }
        return objeto_resposta, 401
