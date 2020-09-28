# en windows
# set FLASK_APP=eggie.py
# set FLASK_ENV=development
# flask run

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, Eggs, Cost, Income, ChickenCoop, Incubator, Nest, UnitaryCost
from func import login_required
from datetime import date

# Configure application
app = Flask(__name__)
app.secret_key = b'a\x01\xcbu\x1f:D\xc9\x00W\xb3K\x16!\xa5\x8c`H\xa8\xbe\xa2X{\xb1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./static/eggy.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("./login.html", message="Debe ingresar un usuario", warning=True)

        # Ensure password was submitted
        elif not password:
            return render_template("./login.html", message="Debe ingresar una contraseña", warning=True)

        # Query database for username
        user = User.query.filter_by(name=username).first()

        # Ensure username exists and
        if not user:
            return render_template("./login.html", message="Usuario no existe", warning=True)

        # Ensure password is correct
        if not check_password_hash(str(user.hash), password):
            return render_template("./login.html", message="Usuario y contraseña no coinciden", warning=True)

        # Remember which user has logged in
        session["user_id"] = user.id
        if user.theme == 'dark-edition':
            session["theme"] = "dark-edition"
        elif user.theme == 'light-edition':
            session["theme"] = "light-edition"

        session["today"] = date.today()
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("./login.html")


@app.route('/', methods=["GET", "POST"])
@login_required
def home():
    eggs = Eggs.query.filter_by(date=session["today"]).first()
    condition = True

    if not eggs:
        condition = False

    if request.method == "POST":

        if condition == False:
            quantity = int(request.form.get("points"))
            eggs = Eggs(quantity, session["user_id"])
            db.session.add(eggs)
            #db.session.merge(eggs)
            db.session.commit()
            return render_template('./index.html', color=session["theme"], quantity=quantity)

        eggs.quantity = eggs.quantity + int(request.form.get("points"))
        db.session.merge(eggs)
        db.session.commit()
        return render_template('./index.html', color=session["theme"], quantity=eggs.quantity)

    if condition == True:
        return render_template('./index.html', color=session["theme"], quantity=eggs.quantity)
    return render_template('./index.html', color=session["theme"], quantity=0)


@app.route('/config.html', methods=["GET", "POST"])
def config():
    user = User.query.filter_by(id=session["user_id"]).first()
    if request.method == "POST":

        password = request.form.get("password")
        newpassword = request.form.get("newpassword")
        confirm = request.form.get("confirm")

        if not password:
            return render_template("config.html", message="Debe ingresar una contraseña", warning=True,
                                   user_id=session["user_id"], username=user.name, color=session["theme"])

        if not newpassword:
            return render_template("config.html", message="Debe ingresar una nueva contraseña", warning=True,
                                   user_id=session["user_id"], username=user.name, color=session["theme"])

        if not confirm:
            return render_template("config.html", message="Debe ingresar nuevamente su nueva contraseña",
                                   warning=True, user_id=session["user_id"], username=user.name, color=session["theme"])

        if not check_password_hash(user.hash, password):
            return render_template("config.html", message="No se encuentra la contraseña", warning=True,
                                   user_id=session["user_id"], username=user.name, color=session["theme"])

        if not newpassword == confirm:
            return render_template("config.html", message="Las nueva contraseñas no es igual a la confirmada", warning=True,
                                   user_id=session["user_id"], username=user.name, color=session["theme"])

        user.hash = generate_password_hash(newpassword)
        db.session.merge(user)
        db.session.commit()

        return render_template("./config.html", message="Contraseña cambiada", warning=True,
                               user_id=session["user_id"], username=user.name, color=session["theme"])

    return render_template("./config.html", user_id=user.id, username=user.name, color=session["theme"])

@app.route("/color", methods=["GET", "POST"])
@login_required
def color():
    user = User.query.filter_by(id=session["user_id"]).first()

    if request.method == "POST":

        if user.theme == 'dark-edition':
            session["theme"] = "light-edition"
        elif user.theme == 'light-edition':
            session["theme"] = "dark-edition"

        user.theme = session["theme"]
        db.session.merge(user)
        db.session.commit()

        return redirect("/config.html")
    return redirect("/config.html")



@app.route('/<string:page_name>')
@login_required
def html_page(page_name):
    return render_template(page_name, color=session["theme"])


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")
