import sys
import functions as f
import os
import shutil

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

tab_Spending = []

print("*** Parsing File ***")

f.csv_parser(tab_Spending)

print("*** Gathering Data ***")

tab_month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


tab_money = []
tab_name = []
tab_visit = []

dict_buy = f.gather_account(tab_Spending)

for key, account in dict_buy.items():
    tab_money.append(account.balance)
    tab_name.append(str(key))
    tab_visit.append(account.nb_visit)

print("*** Draw Pie charts ***")

f.draw_pie_charts(tab_name, tab_money, tab_visit)

tab_Spending2016 = []
tab_year = []
dict_Spending = dict()
for ss in tab_Spending:
    year = ss.date.year
    if year not in tab_year:
        tab_year.append(year)
        dict_Spending.update({year: []})
    dict_Spending[year].append(ss)

for year, spending in dict_Spending.items():
    print("*** Building plots for ", year, "***")
    str_year = str(year)
    if os.path.exists(str_year):
        shutil.rmtree(str_year)
    os.mkdir(str_year)
    f.plot_year(spending, str_year)
