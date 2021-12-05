from flask_security import url_for_security, Security, SQLAlchemyUserDatastore
from app.forms import LoginOverrideForm
from app import create_app
import logging
app = create_app()

from app.models import User, Role
from app.extensions import db
security = Security(app, SQLAlchemyUserDatastore(db=db, user_model=User, role_model=Role))


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
