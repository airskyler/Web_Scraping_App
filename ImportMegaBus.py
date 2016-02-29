__author__ = 'Jessy'



__author__ = 'Jessy'


import sqlite3
from json import loads   # importing loads method from json to use in a file object

database_filename = "BusTripData_sql.db"



db = sqlite3.connect(database_filename)
cursor = db.cursor()


# open each mega bus data file and read or fetch all the bus trip data and put that information in a
# variable called " megabusData" to use that information to insert that data to a busTable
for i in range(1, 8):

    with open('Selenium_Scraping\MegaMarch'+str(i)+ '2016.json', 'r') as infile:

        megabusData = loads(infile.read())

    print(str(i))
    for h in megabusData:

        # use number " 1 " as a TripID and use number " 0 " as transfer
        # for the display for the mega bus trip data in treeview.
        # inserting simple and only necessary bus trip data for each day of mega bus trip data to the busTable
        cursor.execute('''INSERT INTO busTable VALUES (?,?,?,?,?,?,?,?,?) ''',
                       (1, 'MegaBus', '3/' +str(i)+ '/2016',
        h.get('leave').strip(), h.get('arrive').strip(), h.get('from')[:12].strip(), h.get('to')[:8].strip(),
        0,
        h.get('price').replace('From', '').strip()))



        db.commit()


db.close()




