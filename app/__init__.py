import logging
from flask import Flask
from .models import User, Role
from flask_security import SQLAlchemyUserDatastore, url_for_security
from .forms import ShareMyIdeaForm, sendDocumentForm
from .extensions import db, migrate, security, mail, mysql, bootstrap
from flask_security import LoginForm, ForgotPasswordForm
from .forms import LoginOverrideForm, RegisterOverrideForm


def create_app():
    app = Flask(__name__)
    app.debug = True

    @app.context_processor
    def inject_foo():
        return {
            'url_for_security': url_for_security,
            'login_user_form': LoginOverrideForm(),
            'register_user_form': RegisterOverrideForm(),
        }

    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.config.from_pyfile('config.py')
    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    security.init_app(app=app,
                      login_form=LoginOverrideForm,
                      forgot_password_form=ForgotPasswordForm,
                      register_form=RegisterOverrideForm,
                      confirm_register_form=RegisterOverrideForm,
                      datastore=SQLAlchemyUserDatastore(db=db, user_model=User, role_model=Role))
    mysql.init_app(app)

    from app.routes.home import bp as home_bp
    app.register_blueprint(home_bp, url_prefix='/')

    return app








