from flask import request, render_template
from index import app, db
from flask_admin import Admin
from models import User, Role, File, FileView, AdminModelView
from admin_extend import MyAdminIndexView
from flask import send_file
import io
from flask.ext.login import LoginManager


# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


init_login()

admin = Admin(app, index_view=MyAdminIndexView(),
              base_template='my_master.html',
              name='Salut Ambiental', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(FileView(model=File, session=db.session))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# download route
@app.route("/download/<int:id>", methods=['GET'])
def download_blob(id):
    file = File.query.get_or_404(id)
    return send_file(
        io.BytesIO(file.blob),
        attachment_filename=file.filename,
        mimetype=file.mimetype
    )


if __name__ == '__main__':
    app.run()
