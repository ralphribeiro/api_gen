from flask.wrappers import Response
from app.api.model.usuario import Usuario
from ..service.lista_negra_service import salva_token


class Autenticacao:
    @staticmethod
    def login_usuario(dado):
        try:
            usuario = Usuario.query.filter_by(email=dado.get('email')).first()
            if usuario and usuario.verifica_chave(dado.get('chave')):
                token_autenticacao = usuario.codifica_token_autenticacao(
                    usuario.id)
                if token_autenticacao:
                    objeto_resposta = {
                        'status': 'sucesso',
                        'message': 'Login feito com sucesso.',
                        'Authorization': token_autenticacao.decode()
                    }
                    return objeto_resposta, 200
                else:
                    # senha inválida
                    objeto_resposta = {
                        'status': 'falha',
                        'message': 'Usuário ou/e Senha inválido(s).'
                    }
                    return objeto_resposta, 401
            else:
                # usuário inválido
                objeto_resposta = {
                    'status': 'falha',
                    'message': 'Usuário ou/e Senha inválido(s).'
                }
                return objeto_resposta, 401
        except Exception as e:
            objeto_resposta = {
                'status': 'falha',
                'message': 'Tente novamente mais tarde.'
            }
            return objeto_resposta, 500

    @staticmethod
    def logout_usuario(dado):
        if dado:
            token_autenticacao = dado.split(" ")[1]
        else:
            token_autenticacao = ''

        if token_autenticacao:
            resp = Usuario.decodifica_token_autenticacao(token_autenticacao)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return salva_token(token=token_autenticacao)
            else:
                objeto_resposta = {
                    'status': 'falha',
                    'message': resp
                }
                return objeto_resposta, 401
        else:
            objeto_resposta = {
                'status': 'falha',
                'menssagem': 'Forneça um token de autenticação válido.'
            }
            return objeto_resposta, 403


    @staticmethod
    def obtem_usuario_logado(nova_requisicao):
        token_autenticacao = nova_requisicao.headers.get('Autorizacao')
        if token_autenticacao:
            resp = Usuario.decodifica_token_autenticacao(token_autenticacao)
            if not isinstance(resp, str):
                usuario = Usuario.query.filter_by(id=resp).first()
                objeto_resposta = {
                    'status': 'sucesso',
                    'dado': {
                        'usuario_id': usuario.id,
                        'email': usuario.email,
                        'admin': usuario.admin,
                        'registrado_em': str(usuario.registered_on)
                    }
                }
                return objeto_resposta, 200
            objeto_resposta = {
                'status': 'falha',
                'message': resp
            }
            return objeto_resposta, 401
        else:
            objeto_resposta = {
                'status': 'falha',
                'message': 'Forneça um token de autenticacao válido.'
            }
            return objeto_resposta, 401
