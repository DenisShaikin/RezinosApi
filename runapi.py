#!flask/bin/python
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db
from app.models import Tire

# from app.models import  User, Tire, Rim

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config )
Migrate(app, db, render_as_batch=True)
# mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
    return {'Tire': Tire}  #'db': db, 'User': User, 'Tire': Tire, 'Rim':Rim}


if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )

if __name__ == "__main__":
    app.run()

