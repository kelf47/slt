from index import db
from flask_user import UserMixin
from wtforms import ValidationError, fields
from wtforms.widgets import FileInput
from werkzeug.datastructures import FileStorage
from wtforms.validators import required
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from flask.ext.security import current_user


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'',
                      unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    login = db.Column(db.String(80), unique=True)
    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    documents = db.relationship('File', secondary='users_files',
                                backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return u"Nom : {first_name} {last_name};  Email: {email})".format(
            first_name=self.first_name, last_name=self.last_name,
            filename=self.email)


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'',
                     unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')

    def __str__(self):
        return self.name


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id',
                        ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id',
                        ondelete='CASCADE'))


# ------------------ FILE STORING -------------------------------

class BlobMixin(object):
    mimetype = db.Column(db.Unicode(length=255), nullable=False)
    filename = db.Column(db.Unicode(length=255), nullable=False)
    blob = db.Column(db.LargeBinary(), nullable=False)
    size = db.Column(db.Integer, nullable=False)


class File(db.Model, BlobMixin):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(length=255), nullable=False, unique=True)
    public = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __str__(self):
        return u"nom: {name}; document: {filename})".format(
            name=self.name, filename=self.filename)


class UsersFiles(db.Model):
    __tablename__ = 'users_files'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id',
                        ondelete='CASCADE'))
    file_id = db.Column(db.Integer(), db.ForeignKey('files.id',
                        ondelete='CASCADE'))


class BlobUploadField(fields.StringField):

    widget = FileInput()

    def __init__(self, label=None, allowed_extensions=None,
                 size_field=None, filename_field=None, mimetype_field=None,
                 **kwargs):

        self.allowed_extensions = allowed_extensions
        self.size_field = size_field
        self.filename_field = filename_field
        self.mimetype_field = mimetype_field
        validators = [required()]

        super(BlobUploadField, self).__init__(label, validators, **kwargs)

    def is_file_allowed(self, filename):
        """
            Check if file extension is allowed.

            :param filename:
                File name to check
        """
        if not self.allowed_extensions:
            return True

        return ('.' in filename and
                filename.rsplit('.', 1)[1].lower() in
                map(lambda x: x.lower(), self.allowed_extensions))

    def _is_uploaded_file(self, data):
        return (data and isinstance(data, FileStorage) and data.filename)

    def pre_validate(self, form):
        super(BlobUploadField, self).pre_validate(form)
        if self._is_uploaded_file(self.data) and not self.is_file_allowed(
                self.data.filename):
            raise ValidationError('Format no valid')

    def process_formdata(self, valuelist):
        if valuelist:
            data = valuelist[0]
            self.data = data

    def populate_obj(self, obj, name):

        if self._is_uploaded_file(self.data):

            _blob = self.data.read()

            setattr(obj, name, _blob)

            if self.size_field:
                setattr(obj, self.size_field, len(_blob))

            if self.filename_field:
                setattr(obj, self.filename_field, self.data.filename)

            if self.mimetype_field:
                setattr(obj, self.mimetype_field, self.data.content_type)


class AdminModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role('admin')
        return False


class FileView(AdminModelView):

    column_list = ('name', 'size', 'filename', 'mimetype', 'download')
    form_columns = ('name', 'blob')

    form_extra_fields = {'blob': BlobUploadField(
        label='File',
        allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'],
        size_field='size',
        filename_field='filename',
        mimetype_field='mimetype'
    )}

    def _download_formatter(self, context, model, name):
        return Markup("<a href='{url}' target='_blank'>Download</a>".format(
            url=self.get_url('download_blob', id=model.id)))

    column_formatters = {
        'download': _download_formatter,
    }
