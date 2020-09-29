"""Initialize app."""
# en windows
# set FLASK_APP=eggie.py
# set FLASK_ENV=development
# flask run

from flask import redirect, render_template, flash, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import db, app, User, Eggs, Cost, Sales, ChickenCoop, Incubator, Nest, UnitaryPrice
from datetime import date, datetime
from func import data_eggs, data_chickens, sales, list_sales_month, list_cost_month, cost_month, chickens_coop, roosters_total, incubator_total, chickens_nest, finances


login_manager = LoginManager()
login_manager.init_app(app)

# global data
theme, today = "dark-edition", date.today()

@app.route("/login", methods=["GET", "POST"])
def login():

    # make sure that is start unloged
    if request.method == "POST":

        if not current_user.is_authenticated:

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

            if not user.check_password(password):
                return render_template("./login.html", message="Usuario y contraseña no coinciden", warning=True)

            login_user(user)

            global theme, today

            today = date.today()
            theme = user.theme

            return redirect("/")
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("./login.html")


@app.route('/', methods=["GET", "POST"])
@login_required
def home():

    global theme, today
    eggs = data_eggs(today)
    anim = data_chickens()
    finan = finances(today)

    if request.method == "POST":

        if not request.form.get("points"):
            return redirect("/")

        quantity = int(request.form.get("points"))

        # new eggs with no data in database
        if eggs[0] == 0:
            eggie = Eggs(quantity)
            db.session.add(eggie)
            db.session.commit()
            eggs = data_eggs(today)
            return render_template('./index.html', color=theme, eggs=eggs, anim=anim, finan=finan)

        # update today eggs
        eggie = Eggs.query.filter_by(date=today).first()
        eggie.quantity = eggie.quantity + int(request.form.get("points"))
        db.session.commit()
        eggs = data_eggs(today)
        return render_template('./index.html', color=theme, eggs=eggs, anim=anim, finan=finan)

    return render_template('./index.html', color=theme, eggs=eggs, anim=anim, finan=finan)


@app.route('/gallineros.html', methods=["GET", "POST"])
@login_required
def gallineros():
    
    global theme, today

    data = ChickenCoop.query.all()
    totalc = chickens_coop()
    totalr = roosters_total()
    condition = True

    if not data:
        condition = False

    if request.method == "POST":

        if not request.form.get("name") or not request.form.get("chickens") or not request.form.get("roosters"):
            if condition == False:
                return render_template("./gallineros.html", message="Debe ingresar todos los datos", warning=True,
                                       color=theme, coop=[], totalc=totalc, totalr=totalr)
            return render_template("./gallineros.html", message="Debe ingresar todos los datos", warning=True,
                                   color=theme, coop=data, totalc=totalc, totalr=totalr)

        name = request.form.get("name")
        chickens = int(request.form.get("chickens"))
        roosters = int(request.form.get("roosters"))
        coop = []

        # new coop with no data in database
        if condition == False:

            update = ChickenCoop(name, chickens, roosters)
            db.session.add(update)
            db.session.commit()
            coop.append(update)
            return render_template('./gallineros.html', color=theme, coop=coop, totalc=totalc, totalr=totalr)

        update = ChickenCoop.query.filter_by(name=name).first()

        # new coop
        if not update:
            update = ChickenCoop(name, chickens, roosters)
            db.session.add(update)
            db.session.commit()
            data = ChickenCoop.query.all()
            return render_template('./gallineros.html', color=theme, coop=data, totalc=totalc, totalr=totalr)

        # update coop
        update = ChickenCoop.query.filter_by(name=name).first()
        update.name = name
        update.chickens = chickens
        update.roosters = roosters
        db.session.merge(update)
        db.session.commit()
        data = ChickenCoop.query.all()
        return render_template('./gallineros.html', color=theme, coop=data, totalc=totalc, totalr=totalr)

    if condition == True:
        return render_template('./gallineros.html', color=theme, coop=data, totalc=totalc, totalr=totalr)
    return render_template('./gallineros.html', color=theme, coop=[], totalc=totalc, totalr=totalr)


@app.route('/delete_gall', methods=["GET", "POST"])
@login_required
def delete_gall():

    if request.method == "POST":

        if not request.form.get("gall_id"):
            return redirect("./gallineros.html")

        gall = ChickenCoop.query.filter_by(id=request.form.get("gall_id")).first()

        if not gall:
            return redirect("./gallineros.html")

        db.session.delete(gall)
        db.session.commit()
        return redirect("./gallineros.html")
    return redirect("./gallineros.html")


@app.route('/incubadoras.html', methods=["GET", "POST"])
@login_required
def incubadoras():
    global theme, today

    data = Incubator.query.all()
    total = incubator_total()
    condition = True

    if not data:
        condition = False

    if request.method == "POST":

        if not request.form.get("name") or not request.form.get("quantity") or not request.form.get("date_start") or not request.form.get("date_end"):
            if condition == False:
                return render_template("./incubadoras.html", message="Debe ingresar todos los datos", warning=True,
                                       color=theme, inc=[], today=today, total=total)
            return render_template("./incubadoras.html", message="Debe ingresar todos los datos", warning=True,
                                   color=theme, inc=data, today=today, total=total)

        name = request.form.get("name")
        eggs = int(request.form.get("quantity"))
        date_start = datetime.strptime(request.form.get("date_start"), '%Y-%m-%d')
        date_end = datetime.strptime(request.form.get("date_end"), '%Y-%m-%d')
        inc = []

        # new incubator with no data in database
        if condition == False:
            update = Incubator(name, eggs, date_start, date_end)
            db.session.add(update)
            db.session.commit()
            inc.append(update)
            return render_template('./incubadoras.html', color=theme, inc=inc, today=today, total=total)

        update = Incubator.query.filter_by(name=name).first()

        # new incubator
        if not update:
            update = Incubator(name, eggs, date_start, date_end)
            db.session.add(update)
            db.session.commit()
            data = Incubator.query.all()
            return render_template('./incubadoras.html', color=theme, inc=data, today=today, total=total)

        # update incubator
        update = Incubator.query.filter_by(name=name).first()
        update.name = name
        update.eggs = eggs
        update.date_start = date_start
        update.date_end = date_end
        db.session.merge(update)
        db.session.commit()
        data = Incubator.query.all()
        return render_template('./incubadoras.html', color=theme, inc=data, today=today, total=total)

    if condition == True:
        return render_template('./incubadoras.html', color=theme, inc=data, today=today, total=total)
    return render_template('./incubadoras.html', color=theme, inc=[], today=today, total=total)


@app.route('/delete_inc', methods=["GET", "POST"])
@login_required
def delete_inc():
    if request.method == "POST":

        if not request.form.get("inc_id"):
            return redirect("./incubadoras.html")

        inc = Incubator.query.filter_by(id=request.form.get("inc_id")).first()

        if not inc:
            return redirect("./incubadoras.html")

        db.session.delete(inc)
        db.session.commit()
        return redirect("./incubadoras.html")
    return redirect("./incubadoras.html")


@app.route('/ponederos.html', methods=["GET", "POST"])
@login_required
def ponederos():
    global theme, today

    data = Nest.query.all()
    total = chickens_nest()
    condition = True

    if not data:
        condition = False

    if request.method == "POST":

        if not request.form.get("name") or not request.form.get("quantity") or not request.form.get("date_start") or not request.form.get("date_end"):
            if condition == False:
                return render_template("./ponederos.html", message="Debe ingresar todos los datos", warning=True,
                                       color=theme, pon=[], today=today, total=total)
            return render_template("./ponederos.html", message="Debe ingresar todos los datos", warning=True,
                                   color=theme, pon=data, today=today, total=total)

        name = request.form.get("name")
        chickens = int(request.form.get("quantity"))
        date_start = datetime.strptime(request.form.get("date_start"), '%Y-%m-%d')
        date_end = datetime.strptime(request.form.get("date_end"), '%Y-%m-%d')
        inc = []

        # new Nest with no data in database
        if condition == False:
            update = Nest(name, chickens, date_start, date_end)
            db.session.add(update)
            db.session.commit()
            inc.append(update)
            return render_template('./ponederos.html', color=theme, inc=inc, today=today, total=total)

        update = Nest.query.filter_by(name=name).first()

        # new Nest
        if not update:
            update = Nest(name, chickens, date_start, date_end)
            db.session.add(update)
            db.session.commit()
            data = Nest.query.all()
            return render_template('./ponederos.html', color=theme, inc=data, today=today, total=total)

        # update Nest
        update = Nest.query.filter_by(name=name).first()
        update.name = name
        update.eggs = chickens
        update.date_start = date_start
        update.date_end = date_end
        db.session.merge(update)
        db.session.commit()
        data = Nest.query.all()
        return render_template('./ponederos.html', color=theme, inc=data, today=today, total=total)

    if condition == True:
        return render_template('./ponederos.html', color=theme, inc=data, today=today, total=total)
    return render_template('./ponederos.html', color=theme, inc=[], today=today, total=total)


@app.route('/delete_pon', methods=["GET", "POST"])
@login_required
def delete_pon():
    if request.method == "POST":

        if not request.form.get("pon_id"):
            return redirect("./ponederos.html")

        pon = Nest.query.filter_by(id=request.form.get("pon_id")).first()

        if not pon:
            return redirect("./ponederos.html")

        db.session.delete(pon)
        db.session.commit()
        return redirect("./ponederos.html")
    return redirect("./ponederos.html")


@app.route('/costos.html', methods=["GET", "POST"])
@login_required
def costos():

    global theme, today

    data = list_cost_month(today.month)
    total = cost_month(today.month)

    if request.method == "POST":

        if not request.form.get("name") or not request.form.get("quantity") or not request.form.get("unitary")or not request.form.get("total"):
            if data == []:
                return render_template('./costos.html', message="Debe ingresar todos los datos", warning=True,
                                       color=theme, cost=[], total=total)
            return render_template('./costos.html', message="Debe ingresar todos los datos ", warning=True,
                                   color=theme, cost=data, total=total)

        name = request.form.get("name")
        quantity = int(request.form.get("quantity"))
        unitary = int(request.form.get("unitary"))
        total = int(request.form.get("total"))

        new = Cost(name, quantity, unitary, total)
        db.session.add(new)
        db.session.commit()
        data = list_cost_month(today.month)
        return render_template("./costos.html", color=theme, cost=data, total=total)

    return render_template("./costos.html", color=theme, cost=data, total=total)


@app.route('/delete_cost', methods=["GET", "POST"])
@login_required
def delete_cost():

    if request.method == "POST":

        if not request.form.get("cost_id"):
            return redirect("./costos.html")

        cost = Cost.query.filter_by(id=request.form.get("cost_id")).first()

        if not cost:
            return redirect("./costos.html")

        db.session.delete(cost)
        db.session.commit()
        return redirect("./costos.html")
    return redirect("./costos.html")


@app.route('/ventas.html', methods=["GET", "POST"])
@login_required
def ventas():

    global theme, today

    data = list_sales_month(today.month)
    total = sales(today.month)
    prices = UnitaryPrice.query.all()
    condition = True


    if not data:
        condition = False

    if request.method == "POST":

        if not request.form.get("name") or not request.form.get("quantity") or not request.form.get("unitary")or not request.form.get("desc"):
            if condition == False:
                return render_template('./ventas.html', message="Debe ingresar todos los datos", warning=True,
                                       color=theme, sales=[], prices=prices, total=total)
            return render_template('./ventas.html', message="Debe ingresar todos los datos ", warning=True,
                                   color=theme, sales=data, prices=prices, total=total)

        name = request.form.get("name")
        quantity = int(request.form.get("quantity"))
        unitary = int(request.form.get("unitary"))
        desc = int(request.form.get("desc"))
        income = unitary * quantity - desc
        new = Sales(name, quantity, unitary, income, desc)
        db.session.add(new)
        db.session.commit()
        data = Sales.query.order_by(Sales.date).all()
        return render_template("./ventas.html", color=theme, sales=data, prices=prices, total=total)

    if condition == True:
        return render_template("./ventas.html", color=theme, sales=data, prices=prices, total=total)
    return render_template("./ventas.html", color=theme, sales=[], prices=prices, total=total)


@app.route('/delete_sale', methods=["GET", "POST"])
@login_required
def delete_sale():

    if request.method == "POST":

        if not request.form.get("sale_id"):
            return redirect("./ventas.html")

        sale = Sales.query.filter_by(id=request.form.get("sale_id")).first()

        if not sale:
            return redirect("./ventas.html")

        db.session.delete(sale)
        db.session.commit()
        return redirect("./ventas.html")
    return redirect("./ventas.html")


@app.route('/config.html', methods=["GET", "POST"])
def config():

    global theme, today

    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":

        password = request.form.get("password")
        newpassword = request.form.get("newpassword")
        confirm = request.form.get("confirm")

        if not password:
            return render_template("config.html", message="Debe ingresar una contraseña", warning=True,
                                   user_id=current_user.id, username=user.name, color=theme)

        if not newpassword:
            return render_template("config.html", message="Debe ingresar una nueva contraseña", warning=True,
                                   user_id=current_user.id, username=user.name, color=theme)

        if not confirm:
            return render_template("config.html", message="Debe ingresar nuevamente su nueva contraseña",
                                   warning=True, user_id=current_user.id, username=user.name, color=theme)

        if not user.check_password(password):
            return render_template("config.html", message="No se encuentra la contraseña", warning=True,
                                   user_id=current_user.id, username=user.name, color=theme)

        if not newpassword == confirm:
            return render_template("config.html", message="Las nueva contraseñas no es igual a la confirmada", warning=True,
                                   user_id=current_user.id, username=user.name, color=theme)

        user.set_password(newpassword)
        db.session.merge(user)
        db.session.commit()

        return render_template("./config.html", message="Contraseña cambiada", warning=True,
                               user_id=current_user.id, username=user.name, color=theme)

    return render_template("./config.html", user_id=current_user.id, username=user.name, color=theme)


@app.route("/color", methods=["GET", "POST"])
@login_required
def color():

    global theme, today

    user = User.query.filter_by(id=current_user.id).first()

    if request.method == "POST":

        if user.theme == 'dark-edition':
            theme = "light-edition"
        elif user.theme == 'light-edition':
            theme = "dark-edition"

        user.theme = theme
        db.session.merge(user)
        db.session.commit()

        return redirect("/config.html")
    return redirect("/config.html")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return render_template("./login.html")
