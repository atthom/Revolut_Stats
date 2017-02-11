import sys
import functions as f
import os
import shutil

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

tab_Spending = []

print("*** Parsing File ***")

f.csv_parser(tab_Spending)

tab_month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
    print("*** Building for Year", year, "***")
    str_year = str(year)
    if os.path.exists(str_year):
        shutil.rmtree(str_year)
    os.mkdir(str_year)
    f.plot_year(spending, str_year)
