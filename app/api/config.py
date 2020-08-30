import os

postgres_local_base = os.environ['DATABASE_URL']
# DATABASE_URL="postgresql://postgres:senha@localhost/desenv"

base_diretorio = os.path.abspath(os.path.dirname(__file__))


class Config:
    CHAVE_SECRETA = os.getenv('CHAVE_SECRETA', 'nenhuma')
    DEBUG = False


class ConfigDesenvolvimento(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_diretorio, "desenvolvimento.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTestes(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TESTES_URL')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigProducao(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_por_nome = dict(
    desenv=ConfigDesenvolvimento,
    teste=ConfigTestes,
    prod=ConfigProducao
)

chave = Config.CHAVE_SECRETA
