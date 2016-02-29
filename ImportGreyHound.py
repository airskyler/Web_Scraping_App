__author__ = 'Jessy'


import sqlite3
from json import loads       # importing loads method from json to use in a file object

database_filename = "BusTripData_sql.db"



db = sqlite3.connect(database_filename)
cursor = db.cursor()



# open each Greyhound bus data file and read or fetch all the bus trip data and put that information in a
# variable called " greyhoundData" to use that information to insert that data to a busTable
for i in range(1, 8):

    with open('Selenium_Scraping\March'+str(i)+ '2016.json', 'r') as infile:

        greyhoundData = loads(infile.read())

    print(str(i))
    for l in greyhoundData:


# There were error in.get schedule and I had hard time figuring out...  so..  I set the schedule value to equal 1.
# the greyhound schedule information will be displayed in a TripID column with in a treeview.
# inserting simple and only necessary bus trip data for each day of greyhound bus trip data to the busTable
        cursor.execute('''INSERT INTO busTable VALUES (?,?,?,?,?,?,?,?,?) ''',
                       (int(l.get('schedule')) if l.get('schedule')!='' else 1, 'Greyhound', '3/' +str(i)+ '/2016',
        l.get('leave'), l.get('arrive'), l.get('from'), l.get('to'), int(l.get('transfers').replace(' transfers','')),
        l.get('price')))


        db.commit()

db.close()





