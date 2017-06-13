# create_db.py
from app import db
from models import User, Role
import datetime
import hashlib
import hmac
import base64


def generate_sha512_hmac(password_salt, password):
    """ Generate SHA512 HMAC -- for compatibility with Flask-Security """
    return base64.b64encode(hmac.new(password_salt, password.encode('utf-8'),
                            hashlib.sha512).digest())


def add_users():
    admin_role = find_or_create_role('admin', u'Admin')
    find_or_create_role('client', u'Client')
    find_or_create_user(
        u'Admin1', u'Admin1',
        u'admin1@salutambiental.cat', 'salutambiental', admin_role)
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.login == email).first()
    if not user:
        user = User(email=email,
                    login=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user


db.create_all()
add_users()
