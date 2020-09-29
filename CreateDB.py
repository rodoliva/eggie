from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./static/eggy.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    theme = db.Column(db.String, nullable=False, default="dark-edition")

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password, method='sha256')

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Eggs(db.Model):
    __tablename__ = 'eggs'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, quantity):
        self.quantity = quantity


class Cost(db.Model):
    __tablename__ = 'cost'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, default="")
    quantity = db.Column(db.Integer, default=0)
    un_cost = db.Column(db.Integer, default=0)
    tot_cost = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, item, quantity, un_cost, tot_cost):
        self.item = item
        self.quantity = quantity
        self.un_cost = un_cost
        self.tot_cost = tot_cost


class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, default="")
    quantity = db.Column(db.Integer, default=0)
    un_income = db.Column(db.Integer, default=0)
    income = db.Column(db.Integer, default=0)
    desc = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, item, quantity, un_income, income, desc):
        self.item = item
        self.quantity = quantity
        self.un_income = un_income
        self.income = income
        self.desc = desc


class ChickenCoop(db.Model):
    __tablename__ = 'chicken_cop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    chickens = db.Column(db.Integer, default=0)
    roosters = db.Column(db.Integer, default=0)


    def __init__(self, name, chikens, roosters):
        self.name = name
        self.chickens = chikens
        self.roosters = roosters


class Incubator(db.Model):
    __tablename__ = 'incubator'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    eggs = db.Column(db.Integer, default=0)
    date_start = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)

    def __init__(self, name, eggs, date_start, date_end):
        self.name = name
        self.eggs = eggs
        self.date_start =date_start
        self.date_end = date_end


class Nest(db.Model):
    __tablename__ = 'nest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    chickens = db.Column(db.Integer, default=0)
    date_start = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)

    def __init__(self, name, chickens, date_start, date_end):
        self.name = name
        self.chickens = chickens
        self.date_start =date_start
        self.date_end = date_end


class UnitaryPrice(db.Model):
    __tablename__ = 'unitary_price'
    id = db.Column(db.Integer, primary_key=True)
    un_price = db.Column(db.Integer, nullable=False)
    x6 = db.Column(db.Integer, nullable=False)
    x12 = db.Column(db.Integer, nullable=False)
    x24 = db.Column(db.Integer, nullable=False)
    x30 = db.Column(db.Integer, nullable=False)

    def __init__(self, un_price, x6, x12, x24, x30):
        self.un_price = un_price
        self.x6 = x6
        self.x12 = x12
        self.x24 = x24
        self.x30 = x30

def default():
    default_user = User('admin', 'secret')
    db.session.add(default_user)

    start = 200
    for i in range(0, 16):
        aux = start + (i * 10)
        cost = UnitaryPrice(aux, aux * 6, aux * 12, aux * 24, aux * 30)
        db.session.add(cost)

    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    default()