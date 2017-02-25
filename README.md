## Visualize **Revolut Stats**


#### Description

> Little python 3 script, take an export file of [Revolut](https://revolut.com/) and draw some meaningfull plots using [plot.ly API](https://plot.ly/) and print some informations about the spendings.

#### Requirements

Binaries :

 - Allow to launch python 3.X
 - Installed wkthmltopdf
 (If you don't need to export the report in PDF, please comment the code related)

Package python needed :
- plotly
- csv 
- os
- shutil
- datetime
- statistics
- markdown2
- pdfkit


#### How to launch it

>Place your '.csv' file into the same folder as the python script files.
>**You have to change the name of the .csv file in the script in order to use your own data !**
> You should have python on you PATH, or able to launch it in your favorite way.
> It's a python3 script, therefore it should be able to launch with all the 3.X versions.

> `python.exe revolut_stats.py`

> After that, a folder with the name of the CSV has been created with the plots organized by year. They are in .html, use your favorite browser to show them.
> You have also a little report in Markdown at the root of the created folder along with two pie charts. Feel free to check it out !

#### TO DO List

> - compile the script or make a standalone version
> - convert the report into several format (pdf, docx?, html...)
> - draw a pie chart for each payment by day of the week.

#### Known bug
> - since that there is no 'category' section in the .csv given by Revolut. The script is not able to draw things 'by category'
> - same thing for the localisation of the payout !
