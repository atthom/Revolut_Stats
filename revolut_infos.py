import functions as f
import plotly as py

tab_tab = []

print("*** Parsing File ***")

f.csv_parser(tab_tab)


print("*** Gathering Data ***")

tab_money = []
tab_name = []
tab_visit = []
dict_buy = dict()
dict_buy = f.gather_account(tab_tab)

for key, account in dict_buy.items():
    tab_money.append(account.balance)
    tab_name.append(str(key))
    tab_visit.append(account.nb_visit)

print("*** Draw Pie charts ***")

f.draw_pie_charts(tab_name, tab_money, tab_visit)
