from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./static/eggy.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    hash = db.Column(db.String, nullable=False)
    theme = db.Column(db.String, nullable=False, default="dark-edition")

    def __init__(self, name, hash):
        self.name = name
        self.hash = hash


class Eggs(db.Model):
    __tablename__ = 'eggs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, quantity, user_id):
        self.quantity = quantity
        self.user_id = user_id


class Cost(db.Model):
    __tablename__ = 'cost'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, item, quantity, cost, user_id):
        self.item = item
        self.quantity = quantity
        self.cost = cost
        self.user_id = user_id


class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    income = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today())

    def __init__(self, item, quantity, income, user_id):
        self.item = item
        self.quantity = quantity
        self.income = income
        self.user_id = user_id


class ChickenCoop(db.Model):
    __tablename__ = 'chicken_cop'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
    chickens = db.Column(db.Integer, nullable=False)
    roosters = db.Column(db.Integer)


    def __init__(self, name, chikens, roosters, user_id):
        self.name = name
        self.chickens = chikens
        self.roosters = roosters
        self.user_id = user_id


class Incubator(db.Model):
    __tablename__ = 'incubator'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
    eggs = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)

    def __init__(self, name, eggs, date_start, date_end, user_id):
        self.name = name
        self.eggs = eggs
        self.date_start =date_start
        self.date_end = date_end
        self.user_id = user_id


class Nest(db.Model):
    __tablename__ = 'nest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
    chickens = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)

    def __init__(self, name, chickens, date_start, date_end, user_id):
        self.name = name
        self.chickens = chickens
        self.date_start =date_start
        self.date_end = date_end
        self.user_id = user_id


class UnitaryCost(db.Model):
    __tablename__ = 'unitary_cost'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    un_cost = db.Column(db.Integer, nullable=False)
    x6 = db.Column(db.Integer, nullable=False)
    x12 = db.Column(db.Integer, nullable=False)
    x24 = db.Column(db.Integer, nullable=False)
    x30 = db.Column(db.Integer, nullable=False)

    def __init__(self, un_cost, x6, x12, x24, x30):
        self.un_cost = un_cost
        self.x6 = x6
        self.x12 = x12
        self.x24 = x24
        self.x30 = x30

def default():
    default_user = User('admin', generate_password_hash('secret'))
    db.session.add(default_user)

    start = 200
    for i in range(0, 16):
        aux = start + (i * 10)
        cost = UnitaryCost(aux, aux * 6, aux * 12, aux * 24, aux * 30)
        db.session.add(cost)

    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    default()