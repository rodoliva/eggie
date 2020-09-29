from models import Eggs, Cost, Sales, ChickenCoop, Incubator, Nest
from calendar import monthrange

def eggs_today(today):
    eggs = Eggs.query.filter_by(date=today).first()

    if not eggs:
        return 0

    return eggs.quantity


def eggs_month(month):

    total = 0
    eggs = Eggs.query.all()

    if not eggs:
        return 0

    for item in eggs:
        if item.date.month == month:
            total += item.quantity

    return total


def prom_eggs_month(month):

    total = 0
    count = 0
    eggs = Eggs.query.all()

    if not eggs:
        return 0

    for item in eggs:
        if item.date.month == month:
            total += item.quantity
            count += 1

    return round(total / count)


def graph_eggs_month(month):

    total = []
    eggs = Eggs.query.all()

    if not eggs:
        return []

    for item in eggs:
        if item.date.month == month:
            total.append({'day': item.date.day, 'quantity': item.quantity})

    return total


def eggs_total():

    total = 0
    eggs = Eggs.query.all()

    if not eggs:
        return 0

    for item in eggs:
        total += item.quantity

    return total


def graph_eggs_total():
    total = []
    eggs = Eggs.query.all()

    if not eggs:
        return []

    for item in eggs:
        total.append({'day': item.date, 'quantity': item.quantity})

    return total


def sales_today(today):

    sales = Sales.query.filter_by(date=today).first()

    if not sales:
        return 0

    return sales.income


def sales_month(month):

    total = 0
    sales = Sales.query.all()

    if not sales:
        return 0

    for item in sales:
        if item.date.month == month:
            total += item.income

    return total


def list_sales_month(month):

    total = []
    sales = Sales.query.order_by(Sales.date).all()

    if not sales:
        return []

    for item in sales:
        if item.date.month == month:
            total.append(item)

    return total


def eggs_sales_month(month):

    total = 0
    sales = Sales.query.all()

    if not sales:
        return 0

    for item in sales:
        if item.date.month == month:
            total += item.quantity

    return total


def graph_sales_month(year, month):

    month_days = monthrange(year, month)[1]
    total = [0] * month_days
    sales = Sales.query.all()

    if not sales:
        return 0

    for item in sales:
        if item.date.month == month:
            total[item.date.day] += item.income

    return total


def cost_today(today):

    cost =  Cost.query.filter_by(date=today).first()

    if not cost:
        return 0

    return cost.tot_cost


def cost_month(month):

    total = 0
    costs = Cost.query.all()

    if not costs:
        return 0

    for item in costs:
        if item.date.month == month:
            total += item.tot_cost

    return total


def list_cost_month(month):

    total = []
    costs = Cost.query.order_by(Cost.date).all()

    if not costs:
        return []

    for item in costs:
        if item.date.month == month:
            total.append(item)

    return total


def graph_cost_month(year, month):
    month_days = monthrange(year, month)[1]
    total = [0] * month_days
    costs = Cost.query.all()

    if not costs:
        return 0

    for item in costs:
        if item.date.month == month:
            total[item.date.day] += item.income

    return total


def chickens_coop():
    total = 0
    coop = ChickenCoop.query.all()

    if not coop:
        return 0

    for item in coop:
        total += item.chickens
    return total


def chickens_nest():
    total = 0
    nest = Nest.query.all()

    if not nest:
        return 0

    for item in nest:
        total += item.chickens
    return total


def chickens_total():
    total = 0
    coop = ChickenCoop.query.all()
    nest = Nest.query.all()

    if not coop and not nest:
        return 0

    if not coop:
        for item in nest:
            total += item.chickens
        return total

    if not nest:
        for item in coop:
            total += item.chickens
        return total

    for item in nest:
        total += item.chickens

    for item in coop:
        total += item.chickens

    return total


def roosters_total():

    total = 0
    coop = ChickenCoop.query.all()

    if not coop:
        return 0

    for item in coop:
        total += item.roosters

    return total


def incubator_total():

    total = 0
    inc = Incubator.query.all()

    if not inc:
        return 0

    for item in inc:
        total += item.eggs

    return total


def data_eggs(today):
    eggs = []
    eggs.append(eggs_today(today))
    eggs.append(eggs_month(today.month))
    eggs.append(prom_eggs_month(today.month))
    eggs.append(eggs_total())
    return eggs


def data_chickens():
    chickens = []
    chickens.append(chickens_coop())
    chickens.append(chickens_nest())
    chickens.append(chickens_total())
    chickens.append(roosters_total())
    chickens.append(incubator_total())
    return chickens


def sales(month):
    sales = []
    sales.append(eggs_sales_month(month))
    sales.append(sales_month(month))
    return sales


def finances(today):
    finan = []
    finan.append(eggs_sales_month(today.month))
    finan.append(sales_month(today.month))
    finan.append(cost_month(today.month))
    return finan
