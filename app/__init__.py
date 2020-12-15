from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


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
        # TODO register blueprint
        from app.main import main
        app.register_blueprint(main)
        # TODO add command to do things on the database
        pass
    return app

