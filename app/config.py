SECRET_KEY = '7d441f27d441f27567d441f2b6176a'

# SQL Connection Information
MYSQL_DATABASE_USER = 'hamza'
MYSQL_DATABASE_PASSWORD = 'bugs1234'
MYSQL_DATABASE_DB = 'ppp_testing'
MYSQL_DATABASE_HOST = '127.0.0.1'
DB_NAME = 'ppp_testing'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Mail Configuration
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 587
MAIL_USERNAME = 'apikey'
MAIL_PASSWORD = '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'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_SUPPRESS_SEND = False
MAIL_DEFAULT_SENDER = 'sendgrid.service.sff@coretechs.com'
MAIL_DEBUG = True
TESTING = False

# Flask Security Encryption
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "220808495669459354804861340028769321705"

# Flask-Security URLS
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = '/register/'
SECURITY_CHANGE_URL = '/forgot-password/'
SECURITY_CONFIRM_URL = '/confirm/'

# Flask-Security Templates
# Overrides Default Templates

# Flask-Security Configuration
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_RECOVERABLE = True
SECURITY_SEND_PASSWORD_RESET_EMAIL = True
SECURITY_EMAIL_SENDER = ('system@strongfam.org', 'sendgrid.service.sff+support@coretechs.com')
SECURITY_TOKEN_MAX_AGE = 600  # In seconds, 600 = 10 minutes
SECURITY_POST_REGISTER_VIEW = '/login/'
SECURITY_POST_LOGIN_VIEW = '/login-redirect/'
SECURITY_POST_CONFIRM_VIEW = '/login-redirect/'


# Recaptcha Settings
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6Le4UZkaAAAAAINZ0nIy4AvvdY8gEQVxB56npZRP'
RECAPTCHA_PRIVATE_KEY = '6Le4UZkaAAAAALYc9utVJXv8TBFVGpQSqjtygps7'

