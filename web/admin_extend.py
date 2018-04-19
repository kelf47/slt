import os
from app import db
from flask import Flask, url_for, redirect, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from models import User
from flask.ext.admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        user = self.get_user()
        if user is None:
            self.email.errors.append('Usuari invàlid')
            return

        # we're comparing the plaintext pw with the the hash from the db
        if user.password != self.password.data:
            self.password.errors.append('Password invàlid')

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            form.validate_login()
            user = form.get_user()
            if user is not None:
                if user.has_role('admin'):
                    if not form.password.errors and \
                            not form.email.errors:
                        login.login_user(user)
                else:
                    form.password.errors.append(
                        "No tens permisos d'administrador")
            else:
                form.password.errors.append('Credencials invàlides')
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
