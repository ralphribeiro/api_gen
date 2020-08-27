from app.api.model.usuario import Usuario
from flask import request
from flask_restplus import Resource


from ..util.dto import UsuarioDto
from ..service.usuario_service import cria_um_novo_usuario, obtem_usuarios, obtem_usuario


api = UsuarioDto.api
_usuario = UsuarioDto.usuario


@api.route('/')
class ListaUsuario(Resource):
    @api.doc('lista_de_usuarios_registrados')
    @api.marshal_list_with(_usuario, envelope='usuario')
    def get(self):
        """Lista todos os usuários
        """
        return obtem_usuarios()

    # @api.response(201, 'Usuário criado com sucesso')
    # @api.response(409, 'confito')
    @api.doc('cria um novo usuário')
    @api.expect(_usuario, validade=True)
    def post(self):
        """Cria um novo usuário
        """
        dado = request.json
        return cria_um_novo_usuario(dado=dado)


@api.route('/<id_publico>')
@api.param('id_publico', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class Usuario(Resource):
    @api.doc('obtem um usuário')
    @api.marshal_with(_usuario)
    def get(self, id_publico):
        """obtem um usuário pelo identificador
        """
        usuario = obtem_usuario(id_publico)
        if not usuario:
            api.abort(404)
        else:
            return usuario
