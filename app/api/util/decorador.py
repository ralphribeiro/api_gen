from functools import wraps
from flask import request


from app.api.service.autenticacao_helper import Autenticacao


def token_obrigatorio(func):
    @wraps(func)
    def decorado(*args, **kwargs):
        dado, status = Autenticacao.obtem_usuario_logado(request)
        token = dado.get('dado')

        if not token:
            return dado, status

        return func(*args, **kwargs)

    return decorado


def token_admin_obrigatorio(func):
    @wraps(func)
    def decorado(*args, **kwargs):

        dado, status = Autenticacao.obtem_usuario_logado(request)
        token = dado.get('dado')

        if not token:
            return dado, status

        admin = token.get('admin')
        if not admin:
            objeto_resposta = {
                'status': 'falha',
                'message': 'Token de administrador obrigatório'
            }
            return objeto_resposta, 401

        return func(*args, **kwargs)

    return decorado
