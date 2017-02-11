import plotly as py
import plotly.graph_objs as go
import csv
import os
from datetime import datetime
import statistics


class Account:
    def __init__(self, spend):
        if spend is not None:
            self.balance = spend.paidOut
            self.paying = spend.paidIn
            self.reference = spend.reference
            self.nb_visit = 1

    def add(self, spend):
        self.balance += spend.paidOut
        self.paying += spend.paidIn
        self.nb_visit += 1

    def tostring(self):
        if self.balance == 0.0:
            print(self.reference, ", You received ", round(self.paying, 1), "€ and visited", round(self.nb_visit, 1),
                  "times.")
        elif self.paying == 0.0:
            print(self.reference, ", You paid", round(self.balance, 1), "€ and visited", round(self.nb_visit, 1),
                  "times.")


def sortmerchant(dict):
    sorted_balance = sorted(dict.items(), key=lambda x: x[1].balance, reverse=True)
    sorted_visite = sorted(dict.items(), key=lambda x: x[1].nb_visit, reverse=True)

    sorted_merchant_balance_obj = []
    sorted_merchant_visite_obj = []

    for tuplet in sorted_balance:
        strtuple = tuplet[0]
        sorted_merchant_balance_obj.append(dict[strtuple])

    for tuplet in sorted_visite:
        strtuple = tuplet[0]
        sorted_merchant_visite_obj.append(dict[strtuple])

    return [sorted_merchant_balance_obj, sorted_merchant_visite_obj]


def print10(tab, first=True):
    if not first:
        for i in range(len(tab) - 1, len(tab) - 11, -1):
            tab[i].tostring()
    else:
        for i in range(10):
            tab[i].tostring()


def getInfoExchange(dict_buy):
    max_obj = ["", 0, 0]
    min_obj = ["", 10000, 2]

    max_visit = ["", 0, 0]
    min_visit = ["", 199, 10]

    for obj in dict_buy:
        if dict_buy[obj][0] > max_obj[1]:
            max_obj = [obj, dict_buy[obj][0], dict_buy[obj][1]]
        if dict_buy[obj][0] < min_obj[1]:
            min_obj = [obj, dict_buy[obj][0], dict_buy[obj][1]]
        if dict_buy[obj][1] > max_visit[2]:
            max_visit = [obj, dict_buy[obj][0], dict_buy[obj][1]]
        if dict_buy[obj][1] < min_visit[2]:
            min_visit = [obj, dict_buy[obj][0], dict_buy[obj][1]]
    return [max_obj, min_obj, max_visit, min_visit]


def gather_account(tab_tab):
    tab_date = []
    tab_all_money = []
    dict_buy = dict()

    for spending in tab_tab:
        tab_date.append(spending.date)
        tab_all_money.append(spending.balance)
        merchant = str(spending.reference)

        if merchant not in dict_buy:
            dict_buy.update({merchant: Account(spending)})
        else:
            merc = dict_buy[merchant]
            merc.add(spending)
            dict_buy.update({merchant: merc})

    printInfos(dict_buy, tab_all_money)

    return dict_buy


def draw_pie_charts(tab_name, tab_money, tab_visit):
    fig = {
        'data': [{'labels': tab_name,
                  'values': tab_money,
                  'rotation': 235,
                  'type': 'pie'}],
        'layout': {'title': 'Pie Chart on money paid by merchant'}
    }

    py.offline.plot(fig, validate=True, auto_open=False, filename="pie_char_balance_all_times.html", image_width=800,
                    image_height=800)

    fig = {
        'data': [{'labels': tab_name,
                  'values': tab_visit,
                  'type': 'pie'}],
        'layout': {'title': 'Pie Chart on number of visits by merchant'}
    }

    py.offline.plot(fig, validate=True, auto_open=False, filename="pie_char_visit_all_times.html", image_width=800,
                    image_height=800)

def printInfoExchage(obj):
    print("Your most expensive merchant is ", obj[0][0], " with ", obj[0][1], "€ spend and visited ", obj[0][2],
          " times.")
    print("The less expensive merchant is ", obj[1][0], " with only ", obj[1][1], "€ spend and visited ", obj[1][2],
          " times.")
    print("Your most visited merchant is ", obj[2][0], " with ", obj[2][1], "€ spend and visited ", obj[2][2],
          " times.")
    print("The less visited merchant is ", obj[3][0], " with only ", obj[3][1], "€ spend and visited ", obj[3][2],
          " times.")


def printInfos(dict, tab_all_money):
    print("\n*** Info exchange ***")
    tab = sortmerchant(dict)
    print("*** Where you pay the most ***")
    print10(tab[0])
    print("\n*** Where you pay the less ***")
    print10(tab[0], False)
    print("\n*** Where you visit the most ***")
    print10(tab[1])
    print("\n*** Where you visit the less ***")
    print10(tab[1], False)
    print("\n*** Info about current money on account ***")
    printInfoList(tab_all_money)


def printInfoList(list):
    print("\nThe maximum spending : ", max(list), "€")
    print("The minimum spending : ", min(list), "€")
    print("The mean : ", round(statistics.mean(list), 1), "€")
    print("The median : ", round(statistics.median(list), 1), "€")
    print("The low mean : ", round(statistics.median_low(list), 1), "€")
    print("The higher median : ", round(statistics.median_high(list), 1), "€")
    print("The mode is ", round(statistics.mode(list), 1), "€")
    print("The standard deviation is ", round(statistics.stdev(list), 1), "€")
    print("The variance is ", round(statistics.variance(list), 1), "€")


def init_tab(nb, axis, balance, spending):
    for i in range(nb):
        axis.append(i)
        balance.append(0)
        spending.append(0)


class Spending:
    def __init__(self, row):
        self.date = datetime.strptime(row[0], "%d %b %Y ")
        self.reference = row[1]
        try:
            self.paidIn = float(row[3])
            self.paidOut = 0.0
            self.type = "PAID"
        except:
            self.paidOut = float(row[2])
            self.paidIn = 0.0
            self.type = "COST"
        self.balance = float(row[6])


def csv_parser(spendings):
    with open("Revolut-EUR-Statement-Aug 2016 – Jan 2017.csv", 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        iterrow = iter(reader)
        next(iterrow)
        for row in iterrow:
            spendings.append(Spending(row))


def init_tab(nb, axis, balance, spending):
    for i in range(nb):
        axis.append(i)
        balance.append(0)
        spending.append(0)


def barplot(tab1, tab2, title, name):
    data = [go.Bar(x=tab1, y=tab2)]
    label = [dict(x=xi, y=yi,
                  text=str(round(yi, 1)),
                  xanchor='center',
                  yanchor='bottom',
                  showarrow=False,
                  ) for xi, yi in zip(tab1, tab2)]
    py.offline.plot(data, validate=True, auto_open=False, filename=name, image_width=800, image_height=600)
    # help(py.offline.plot)


def scatterplot(tab1, tab2, title, name):
    data = [go.Scatter(x=tab1, y=tab2, mode='lines')]
    py.offline.plot(data, validate=True, auto_open=False, filename=name, image_width=800, image_height=600)


def plot_year(tab_spending, year):
    tab_month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tab_day, tab_week = [], []
    tab_daily_balance, tab_weekly_balance = [], []
    tab_monthly_balance = []
    tab_daily_spending = []
    tab_weekly_spending = []
    tab_monthly_spending = []

    for i in range(13):
        tab_monthly_balance.append(0)
        tab_monthly_spending.append(0)

    init_tab(366, tab_day, tab_daily_balance, tab_daily_spending)
    init_tab(53, tab_week, tab_weekly_balance, tab_weekly_spending)

    for ss in tab_spending:
        isoCal = ss.date.isocalendar()
        month = ss.date.timetuple()[1]
        nbDay = ss.date.timetuple().tm_yday
        tab_daily_balance[nbDay] = ss.balance
        tab_weekly_balance[isoCal[1]] = ss.balance
        tab_monthly_balance[month] = ss.balance
        tab_daily_spending[nbDay] += (ss.paidIn - ss.paidOut)
        tab_weekly_spending[isoCal[1]] += (ss.paidIn - ss.paidOut)
        tab_monthly_spending[month] += (ss.paidIn - ss.paidOut)

    current_balance = 0

    for i in range(366):
        value = tab_daily_balance[i]
        if value > 0:
            current_balance = value
        if value == 0 and current_balance > 0:
            tab_daily_balance[i] = current_balance

    print("*** Building plots by Day ***")
    scatterplot(tab_day,
                tab_daily_balance,
                'Current balance by Day',
                'current_balance_by_day.html')

    os.rename('current_balance_by_day.html', year + '/current_balance_by_day.html')

    scatterplot(tab_day,
                tab_daily_spending,
                'Current variation by Day',
                'current_variation_by_day.html')

    os.rename('current_variation_by_day.html', year + '/current_variation_by_day.html')

    print("*** Building plots by Week ***")
    barplot(tab_week,
            tab_weekly_balance,
            'Current balance by Week',
            'current_balance_by_week_Bar.html')

    os.rename('current_balance_by_week_Bar.html', year + '/current_balance_by_week_Bar.html')

    barplot(tab_week,
            tab_weekly_spending,
            'Current variation by Week',
            'current_variation_by_week_Bar.html')

    os.rename('current_variation_by_week_Bar.html', year + '/current_variation_by_week_Bar.html')

    scatterplot(tab_week,
                tab_weekly_balance,
                'Current balance by Week',
                'current_balance_by_Week_Scatter.html')

    os.rename('current_balance_by_Week_Scatter.html', year + '/current_balance_by_Week_Scatter.html')

    scatterplot(tab_week,
                tab_weekly_spending,
                'Current variation by Week',
                'current_variation_by_Week_Scatter.html')

    os.rename('current_variation_by_Week_Scatter.html', year + '/current_variation_by_Week_Scatter.html')

    print("*** Building plots by Month ***")

    barplot(tab_month_name,
            tab_monthly_balance,
            'Current balance by Month',
            'current_balance_by_month.html')

    os.rename('current_balance_by_month.html', year + '/current_balance_by_month.html')

    barplot(tab_month_name,
            tab_monthly_spending,
            'Current variation by Month',
            'current_variation_by_month.html')

    os.rename('current_variation_by_month.html', year + '/current_variation_by_month.html')
