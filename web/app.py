from flask import request, render_template
from index import app, db
from flask_admin import Admin
from models import User, Role, Document, FileView, AdminModelView
from admin_extend import MyAdminIndexView
from flask import send_file
from flask_babelex import Babel
from flask.ext.login import LoginManager
import io


# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    # Create user loader function

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


init_login()
babel = Babel(app)


@babel.localeselector
def get_locale():
    return 'es'


admin = Admin(app, index_view=MyAdminIndexView(),
              base_template='my_master.html',
              name='Administrador',
              template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(FileView(model=Document, session=db.session))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/qui_som', methods=['GET'])
def qui_som():
    return render_template("qui_som.html")


@app.route('/que_fem', methods=['GET'])
def que_fem():
    return render_template("que_fem.html")


@app.route('/acces', methods=['GET'])
def acces():
    return render_template("qui_som1.html")


@app.route('/contacte', methods=['GET'])
def contactce():
    return render_template("contacte.html")


# download route
@app.route("/download/<int:id>", methods=['GET'])
def download_blob(id):
    file = Document.query.get_or_404(id)
    return send_file(
        io.BytesIO(file.blob),
        attachment_filename=file.filename,
        mimetype=file.mimetype
    )


if __name__ == '__main__':
    app.run()
