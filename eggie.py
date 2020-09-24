# en windows
# set FLASK_APP=eggie.py
# set FLASK_ENV=development
# flask run
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = sqlite3.connect("./static/eggie.db")
c = conn.cursor()

cunit, cost, eggs, income = [], [], [], []

t_cost_un = c.execute("SELECT costo FROM costo_unitario") # id, fecha, costo, seis, doce, veiticuatro, treinta
t_cost = c.execute("SELECT * FROM cost") # id, item, fecha, costo
t_eggs = c.execute("SELECT * FROM eggs") # id, fecha, cantidad
t_income = c.execute("SELECT * FROM eggs") # id, item, fecha, cantidad, costo_un, costo_tot

def getUnCost():
    for i, row in enumerate(t_cost_un):
        cunit[i].append(row['costo'])

def getCost():
    for i, row in enumerate(t_cost):
        cost[i][0].append(row['id'])
        cost[i][1].append(row['item'])
        cost[i][2].append(row['fecha'])
        cost[i][3].append(row['costo'])

def getEggs():
    for i, row in enumerate(t_eggs):
        eggs[i][0].append(row['fecha'])
        eggs[i][1].append(row['cantidad'])

def getIncome():
    for i, row in enumerate(t_income):
        income[i][0].append(row['id'])
        income[i][1].append(row['item'])
        income[i][2].append(row['fecha'])
        income[i][3].append(row['cantidad'])
        income[i][4].append(row['costo_un'])
        income[i][5].append(row['costo_tot'])

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)