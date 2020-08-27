from flask_restplus import Api
from flask import Blueprint

from .api.controller.usuario_controller import api as usuario_ns


blueprint = Blueprint('api', __name__)


api = Api(
    blueprint,
    title='Api Genérica',
    version='0.1',
    description='api genérica para rest com JWT'
)

api.add_namespace(usuario_ns, path='/usuario')