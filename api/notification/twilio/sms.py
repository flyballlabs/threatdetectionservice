from api import app, db #import app and db objects

from flask import Flask
from marketing_notifications_python import get_env
from marketing_notifications_python.config import config_env_files
from marketing_notifications_python.database import set_db
from marketing_notifications_python.views import construct_view_blueprint

apps = {
    'test': None,
    'development': None,
}


def get_app(config_name=None):
    if config_name is None:
        config_name = get_env()

    if apps[config_name] is None:
        apps[config_name] = init_app(config_name)
    return apps[config_name]


def init_app(config_name):
    _configure_app(app, config_name)
    return app


def _configure_app(flask_app, config_name):
    app.config.from_object(config_env_files[config_name])
    set_db(db, config_name)
    flask_app.register_blueprint(construct_view_blueprint(app, db))