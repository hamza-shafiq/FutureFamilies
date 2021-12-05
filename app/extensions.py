from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
mail = Mail()
security = Security()
mysql = MySQL()
