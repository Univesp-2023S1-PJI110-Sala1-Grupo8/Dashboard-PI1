from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from model.user_model import User
from repository._database import Database
from services.user_service import UserService

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "memcached"
app = Flask(__name__, template_folder='./template')
app.secret_key = "dashboard-secret-key-2023"

database = Database()
database.connect()

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
        user_service = UserService(database)
        user = user_service.authenticate(user_email, user_passd)
        if user is not None:
            session["user_id"] = user.id
            session["user_name"] = user.first_name
            return redirect("/home")
        else:
            flash("Acesso negado! Usuário ou senha inválidos. Digite novamente.")
    return render_template("index.html")


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")


@app.route("/home")
def home():
    if not session.get("user"):
        return redirect("/")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
