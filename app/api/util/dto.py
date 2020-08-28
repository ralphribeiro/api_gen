from flask_restplus import Namespace, fields


class UsuarioDto:
    api = Namespace('usuario', description='operações relacionadas ao usuário')
    usuario = api.model('usuario', {
        'email': fields.String(required=True, description='endereço de email'),
        'nome': fields.String(required=True, description='nome'),
        'chave': fields.String(required=True, description='chave'),
        'id_publico': fields.String(description='identificador')
    })


class AutenticacaoDto:
    api = Namespace('autenticacao', description='operações relacionadas à autenticação')
    usuario = api.model('autenticacao_detalhes', {
        'email': fields.String(required=True, description='endereço de email'),
        'chave': fields.String(required=True, description='chave'),
    })
