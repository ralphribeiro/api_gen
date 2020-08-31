from flask import request
from flask_restplus import Resource

from app.api.service.autenticacao_helper import Autenticacao
from ..util.dto import AutenticacaoDto

api = AutenticacaoDto.api
usuario_autenticacao = AutenticacaoDto.usuario


@api.route('/login')
class LoginUsuario(Resource):
    """
        Recurso Login do Usuário.
    """
    @api.doc('login usuário')
    @api.expect(usuario_autenticacao, validate=True)
    def post(self):
        post_dado = request.json
        return Autenticacao.login_usuario(post_dado)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Usuário
    """
    @api.doc('logout do usuário')
    def post(self):
        autenticacao_header = request.headers.get('Authorization')
        return Autenticacao.logout_usuario(autenticacao_header)