import click
import os
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class

from config import set_config

db = SQLAlchemy()
migration = Migrate()
login_manager = LoginManager()
pswManager = Bcrypt()
mail = Mail()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)


@click.command(name='create_db', help='In theory it build the database')
@with_appcontext
def db_creation():
    current_app.config.from_object(set_config())
    db.create_all()


def create_app(config=None):
    app = Flask(__name__)
    try:
        app.config.from_object(config)
    except:
        print('Error in loading the configuration.')
        return None
    db.init_app(app)
    with app.app_context():
        # TODO tests
        # TODO migration
        #migration.init_app(app, db)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.sign_in'
        pswManager.init_app(app)
        mail.init_app(app)

        configure_uploads(app, photos)
        patch_request_class(app, 16*1024*1024)
        # TODO register blueprint
        from app.main import main
        app.register_blueprint(main)

        from app.auth import auth
        app.register_blueprint(auth)

        from app.errors import errors
        app.register_blueprint(errors)

        from app.users import users
        app.register_blueprint(users)

        from app.studyrooms import studyrooms
        app.register_blueprint(studyrooms)
        # TODO add command to do things on the database
        app.cli.add_command(db_creation)
    return app
