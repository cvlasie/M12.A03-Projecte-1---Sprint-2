import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from werkzeug.local import LocalProxy
from flask_debugtoolbar import DebugToolbarExtension
from .helper_mail import MailManager

logger = LocalProxy(lambda: current_app.logger)

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager = Principal()
mail_manager = MailManager()
toolbar = DebugToolbarExtension()

def configure_logging(app):
    log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
    log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)

    log_level = app.config.get('LOG_LEVEL', 'DEBUG').upper()
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError('Nivel de registro no válido')
    app.logger.setLevel(getattr(logging, log_level))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    configure_logging(app)

    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)
    toolbar.init_app(app)

    with app.app_context():
        from . import commands, routes_main, routes_auth, routes_admin, routes_products, routes_category, routes_status

        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_products.products_bp)
        app.register_blueprint(routes_category.category_bp)
        app.register_blueprint(routes_status.status_bp)

        app.cli.add_command(commands.db_cli)

    app.logger.info("Aplicació iniciada")

    return app