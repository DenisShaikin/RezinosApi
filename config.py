import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEtKey_112')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'rezinosPricesDb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIREPRICES_FILE = os.path.join(basedir, 'RossiyaAllTires_Result.csv')


class ProductionConfig(Config):
    DEBUG = False
    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    #MySQL database
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')


class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
