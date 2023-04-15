import time
from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from model.user_model import User
from model.profile_model import Profile
from model.value_objects import UserProfile
from model.value_objects import ProjectStatus
from repository._database import Database
from services.user_service import UserService
from services.project_service import ProjectService

def trace(msg):
    print("DASHBOARD|{}| {}".format(time.strftime("%Y-%m-%d %H:%M"), msg))

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app = Flask(__name__, template_folder='./template', static_folder="./template/static")
app.secret_key = "dashboard-secret-key-2023"
trace("Application is running!")

database = Database()
database.connect()
trace("Database is connected!")

user_service = UserService(database)
project_service = ProjectService(database)

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect("/home")
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form.get("email")
        user_passd = request.form.get("password")
        user = user_service.authenticate(user_email, user_passd)
        if user is not None:
            session["user_id"] = user.id
            session["user_name"] = user.first_name
            session["user_email"] = user.email
            session["user_profile"] = user.profile.name
            session["profile_id"] = user.profile.id
            session["profile_name"] = user.profile.name
            session["user_is_guest"] = user.profile.id == UserProfile.GUEST.id
            session["user_is_po"] = user.profile.id == UserProfile.PRODUCT_OWNER.id
            trace("Session started! User: {} ({})".format(user.first_name, user.profile.name))
            return redirect("/home" if user.profile.id != 1 else "/admin")
        else:
            trace("Access Denied for User {}.".format(user_email))
            flash("Acesso negado! Usuário ou senha inválidos. Digite novamente.")
    return render_template("index.html")


@app.route("/logout")
def logout():
    trace("Session finished! User: {} ({})".format(session['user_name'], session['user_profile']))
    session["user_id"] = None
    return redirect("/")


@app.route("/home")
def home():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("home.html")


@app.route("/admin")
def admin():
    if not session.get("user_id"):
        return redirect("/login")
    if session.get("user_profile").lower() != "admin":
        return redirect("/login")

    users = user_service.admin_get_all_users()
    profiles = UserProfile.List

    return render_template("admin.html", users=users, profiles=profiles)


@app.route("/usuario/trocar-perfil", methods=["POST"])
def change_profile():
    user_id = request.form['user_id']
    new_profile_id = request.form['new_profile']
    trace("Changing Profile of User {} to {}".format(user_id, new_profile_id))

    profile = Profile(new_profile_id, '')
    user = user_service.find_user_by_id(user_id)
    user = user_service.change_user_profile(user, profile)

    return redirect("/admin")


@app.route("/usuario/novo", methods=["POST"])
def new_user():
    new_user_first_name = request.form['textNewUserFirstName']
    new_user_last_name = request.form['textNewUserLastName']
    new_user_email = request.form['textNewUserEmail']
    new_user_pass = request.form['textNewUserPassword']
    trace("Adding new User (FirstName: {}, LastName: {}, E-mail: {}".format(
           new_user_first_name, new_user_last_name, new_user_email))

    guest_profile = UserProfile.GUEST
    new_user = User(id=0, first_name=new_user_first_name, last_name=new_user_last_name,
                    email=new_user_email, password=new_user_pass, profile=guest_profile)
    new_user = user_service.add_new_user(new_user)

    if new_user is None:
        flash("Falha ao cadastrar novo usuário. Contacte o Administrador.")
        return redirect("/")

    trace(" --- New Password: '{}' ".format(new_user.password))
    flash(".Novo Usuário cadastrado. Verifique seu e-mail.")

    return redirect("/")

@app.route("/usuario/zerar-senha", methods=["POST"])
def forgot_password():
    user_email = request.form['textUserEmail']

    trace("Reseting User Password (E-mail: {}".format(user_email))

    user = user_service.find_user_by_email(user_email)
    if user is None:
        flash("Usuário não localizado.")
        return redirect("/")

    new_password = user_service.reset_password(user)

    flash(".Senha zerada com sucesso! Verifique seu e-mail.")

    return redirect("/")


@app.route("/usuario/trocar-senha", methods=["POST"])
def change_password():
    user_email = request.form['textUserEmail']
    user_old_pass = request.form['textUserOldPassword']
    user_new_pass = request.form['textUserNewPassword']
    user_confirm_pass = request.form['textUserConfirmPassword']

    if user_new_pass != user_confirm_pass:
        flash("As senhas não coincidem.")
        return redirect("/home")

    trace("Changing  User Password (E-mail: {}".format(user_email))

    user = user_service.find_user_by_email(user_email)
    if user is None:
        flash("Usuário não localizado.")
        return redirect("/home")

    user = user_service.authenticate(user_email, user_old_pass)
    if user is None:
        flash("Acesso negado! Usuário ou senha inválidos.")
        return redirect("/home")

    changed_pass = user_service.change_user_password(user, user_new_pass)
    if not changed_pass:
        flash("Falha ao trocar a senha. Contacte o Administrador.")
        return redirect("/home")

    flash(".Senha alterado com sucesso!")

    return redirect("/home")


@app.route("/usuario/remover", methods=["POST"])
def remove_user():
    user_id_to_remove = request.form['user_id_to_remove']
    trace("Removing User: {}".format(user_id_to_remove))

    user = user_service.find_user_by_id(user_id_to_remove)
    if user is None:
        flash("Falha ao remover o usuário (ID não localizado). Contacte o Administrador.")
        return redirect("/admin")

    user_was_removed = user_service.remove_user(user)
    if not user_was_removed:
        flash("Falha ao remover o usuário (Deleção falhou). Contacte o Administrador.")
        return redirect("/home")

    return redirect("/admin")


@app.route("/projetos", methods=["GET"])
def list_projects():
    user_id = session["user_id"]
    user = user_service.find_user_by_id(user_id)
    if user is None:
        flash("Sessão Inválida.")
        return redirect("/")
    if user.profile.id != UserProfile.PRODUCT_OWNER.id:
        flash("Sem permissão para esta opção.")
        return redirect("/")
    projects = project_service.get_all_projects_of_user(user)
    if projects is None:
        flash("Falha ao carregar os projetos.")
        return redirect("/projetos")
    return render_template("projects.html", projects=projects, project_status=ProjectStatus)


if __name__ == "__main__":
    app.run(debug=True)
