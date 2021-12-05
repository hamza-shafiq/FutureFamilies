from flask_security import UserMixin, RoleMixin
from .extensions import db
from sqlalchemy import func
import secrets
import datetime

secrets.token_hex(12)
roles_users = db.Table(
    'userrole',
    db.Column('emailaddress', db.VARCHAR(50), db.ForeignKey('user.emailaddress')),
    db.Column('rolecode', db.INT(), db.ForeignKey('role.rolecode'))
)


class User(db.Model, UserMixin):
    # id = db.Column(db.INT(), primary_key=True)
    email = db.Column('emailaddress', db.VARCHAR(50), primary_key=True)
    password = db.Column(db.VARCHAR(22))
    active = db.Column(db.BOOLEAN, default=True)
    reg_complete = db.Column(db.BOOLEAN, default=False)
    authenticated = db.Column(db.BOOLEAN, default=False)
    anonymous = db.Column(db.BOOLEAN, default=False)
    created_at = db.Column('created_at', db.DATETIME(timezone=True), default=datetime.datetime.utcnow)
    confirmed_at = db.Column(db.TIMESTAMP())
    last_login = db.Column('lastlogin', db.TIMESTAMP())
    preferred_name = db.Column('preferredname', db.VARCHAR(16))
    title = db.Column(db.CHAR(3), default='mr')
    first_name = db.Column('firstname', db.VARCHAR(14))
    mi = db.Column(db.CHAR(1))
    last_name = db.Column('lastname', db.VARCHAR(16))
    name_suffix = db.Column('namesuffix', db.CHAR(3))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=secrets.token_hex(120))
    roles = db.relationship(argument='Role',
                            secondary=roles_users,
                            backref=db.backref(name='user',
                                               lazy='dynamic'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Role(db.Model, RoleMixin):
    entry_page_name = db.Column('entrypagename', db.VARCHAR(35))
    role_code = db.Column('rolecode', primary_key=True)
    roledesc = db.Column('roledesc', db.VARCHAR(35))
    roleshortdesc = db.Column('roleshortdesc', db.VARCHAR(30), unique=True)

    def __str__(self):
        return self.name
    pass
