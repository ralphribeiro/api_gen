from flask_restplus import Namespace, fields


class UsuarioDto:
    api = Namespace('usuario', description='operações relacionadas ao usuário')
    usuario = api.model('user', {
        'email': fields.String(required=True, description='endereço de email'),
        'nome': fields.String(required=True, description='nome'),
        'chave': fields.String(required=True, description='chave'),
        'id_publico': fields.String(description='identificador')
    })
