import functions as f
import plotly as py

tab_tab = []

print("*** Parsing File ***")

f.csv_parser(tab_tab)

tab_date = []
tab_all_money = []
dict_buy = dict()

print("*** Gathering Data ***")

i = 0
for spending in tab_tab:
    tab_date.append(spending.date)
    tab_all_money.append(spending.balance)
    merchant = str(spending.reference)

    if merchant not in dict_buy:
        dict_buy.update({merchant: f.Account(spending) })
    else:
        merc = dict_buy[merchant]
        merc.add(spending)
        dict_buy.update({merchant: merc})


f.printInfos(dict_buy, tab_all_money)

tab_money = []
tab_name = []
tab_visit = []

for key, account in dict_buy.items():
    tab_money.append(account.balance)
    tab_name.append(str(key))
    tab_visit.append(account.nb_visit)

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