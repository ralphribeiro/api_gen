from app.api import db
from app.api.model.lista_negra import ListaNegraToken


def salva_token(token):
    lista_negra_token = ListaNegraToken(token=token)
    try:
        # insert the token
        db.session.add(lista_negra_token)
        db.session.commit()
        response_object = {
            'status': 'sucesso',
            'message': 'Sessão encerrada com sucesso.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'falha',
            'message': e
        }
        return response_object, 200