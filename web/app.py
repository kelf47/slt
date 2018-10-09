from flask import request, render_template, redirect
from index import app, db
from flask_admin import Admin
from models import User, Document, FileView, AdminModelView, TipusDocument, \
    TipusDocumentView
from admin_extend import MyAdminIndexView
from flask import send_file
from flask_babelex import Babel
from flask.ext.login import LoginManager
from flask_login import login_user, logout_user, current_user
from flask import abort
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
admin.add_view(TipusDocumentView(model=TipusDocument, session=db.session))


@app.route('/inici', methods=['GET', 'POST'])
def index_cat():
    return render_template('inici.html')


@app.route('/inicio', methods=['GET', 'POST'])
def index_cast():
    return render_template('inicio.html')


@app.route('/qui_som', methods=['GET'])
def qui_som():
    return render_template("qui_som.html")


@app.route('/quienes_somos', methods=['GET'])
def quienes_somos():
    return render_template("quienes_somos.html")


@app.route('/que_fem', methods=['GET'])
def que_fem():
    return render_template("que_fem.html")


@app.route('/que_hacemos', methods=['GET'])
def que_hacemos():
    return render_template("que_hacemos.html")


def get_user_docs(user):
    public = list(Document.query.with_entities(
        Document.nom, Document.tipus_id, Document.id,
        Document.size, Document.creat).filter_by(compartit=True))
    private = list(user.documents.with_entities(
        Document.nom, Document.tipus_id, Document.id,
        Document.size, Document.creat).all())
    docs = list(set(public + private))
    for doc in docs:
        tipus_query = TipusDocument.query.filter_by(id=doc.tipus_id)
        if tipus_query:
            tipus = tipus_query[0]
            doc.tipus_id = tipus.tipus
    docs.sort()
    return docs


def get_user_tipus(docs):
    tipus = set()
    for doc in docs:
        if doc.tipus_id:
            tipus.add(doc.tipus_id)
    return tipus


@app.route('/acces', methods=['GET', 'POST'])
def acces():
    error = ""
    docs = []
    tipus_document = []
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            if (user.password == password):
                login_user(user)
                docs = get_user_docs(user)
                tipus_document = get_user_tipus(docs)
            else:
                error = 'Usuari o contrassenya incorrecta.'
        else:
            error = 'Usuari o contrassenya incorrecta.'
    else:
        if current_user.is_authenticated:
            docs = get_user_docs(current_user)
            tipus_document = get_user_tipus(docs)

    return render_template("acces.html", docs=docs,
                           tipus_document=tipus_document, error=error)


@app.route('/acceso', methods=['GET', 'POST'])
def acceso():
    error = ""
    docs = []
    tipus_document = []
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            if (user.password == password):
                login_user(user)
                docs = get_user_docs(user)
                tipus_document = get_user_tipus(docs)
            else:
                error = 'Usuario o contraseña incorrecta.'
        else:
            error = 'Usuario o contraseña incorrecta.'
    else:
        if current_user.is_authenticated:
            docs = get_user_docs(current_user)
            tipus_document = get_user_tipus(docs)

    return render_template("acceso.html", docs=docs,
                           tipus_document=tipus_document, error=error)


@app.route('/logout_cat', methods=['POST'])
def logout_cat():
    logout_user()
    return redirect('acces')


@app.route('/logout_cast', methods=['POST'])
def logout_cast():
    logout_user()
    return redirect('acceso')


@app.route('/contacte', methods=['GET'])
def contace():
    return render_template("contacte.html")


@app.route('/contacto', methods=['GET'])
def contacto():
    return render_template("contacto.html")


# download route
@app.route("/download/<int:id>", methods=['GET'])
def download_blob(id):
    print (current_user)
    if current_user.is_authenticated and (current_user.has_role('admin') or
                                          id in [doc.id for doc in
                                          get_user_docs(current_user)]):

        print ("inside")
        file = Document.query.get_or_404(id)
        return send_file(
            io.BytesIO(file.blob),
            attachment_filename=file.filename,
            mimetype=file.mimetype
        )
    abort(404)


if __name__ == '__main__':
    app.run()
