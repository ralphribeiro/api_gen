import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

base_diretorio = os.path.abspath(os.path.dirname(__file__))


class Config:
    CHAVE_SECRETA = os.getenv('CHAVE_SECRETA', 'meu_precioso_preciso')
    DEBUG = False


class ConfigDesenvolvimento(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_diretorio, "desenvolvimento.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTestes(Config):
    DEBUG = True
    TESTANDO = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_diretorio, "testes.db")}'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigProducao((Config)):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_por_nome = dict(
    dev=ConfigDesenvolvimento,
    teste=ConfigTestes,
    prod=ConfigProducao
)

chave = Config.CHAVE_SECRETA
