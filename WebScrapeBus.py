__author__ = 'Jessy'


###   For this project I got some help by a looking at URL source of
###   https://github.com/minneapolis-edu/sql_injection/blob/master/login.py

###   The reference for the treeview code URL is http://stackoverflow.com/questions/34200569/python-treeview-and-grid


###   I also got some help from Mason from learning center and Boyd from my classmate to do this project

###   Importing tkinter to use GUI interface with Python code

###   Importing sqlite3 for database function




from dateutil import parser

import sqlite3

from tkinter import*

# importing Treeview from tkinter to display a database table on GUI Frame
from tkinter.ttk import Treeview


# Database name
database_filename = "BusTripData_sql.db"



# Creating a GUI frame with
class hyGUI(Frame):


    def __init__(self):


        Frame.__init__(self)
        self.master.title("Bus Trip Information")

        self.master.maxsize(1400, 1000)      # Maximum Frame size
        self.pack()
        self._treeview = Treeview(self)      # initialize the treeview


        # Adding space to GUI frame
        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()




        # Writing label on gui and creating a data insert box to get user input when clicking a button

        self.BusDate = Label(self, text = "Please pick a date between 3/1/2016 to 3/7/2016 to search a bus trip")
        self.BusDate.pack()

        # User input box for Bus Date search
        self.BusDateVar = StringVar()
        self.BusDateEntry = Entry(self, textvariable = self.BusDateVar, width=30)
        self.BusDateEntry.pack()



        # Adding space to GUI frame
        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()



        self.BusTime = Label(self, text = "Please pick a bus departing time")
        self.BusTime.pack()

        # User input box for Bus Departing time search
        self.BusTimeVar = StringVar()
        self.BusTimeEntry = Entry(self, textvariable = self.BusTimeVar, width=30)
        self.BusTimeEntry.pack()


        # Creating space between the button and insert box on the GUI frame
        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()




        # Search button
        self._searchButton = Button(self, text="Search", command=self._search)
        self._searchButton.pack()


        # Adding space between button
        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()


        # Exit button
        self._exitButton = Button(self, text="Exit", command=self._exit)
        self._exitButton.pack()


        # Adding space between button and treeview data table
        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()


        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()


        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()



# The reference for the treeview code URL is http://stackoverflow.com/questions/34200569/python-treeview-and-grid

        self._treeview['columns']=('Trip_ID', 'Carrier', 'Date', 'Depart_Time', 'Arrive_Time', 'From',
                                   'To', '#_of_Transfer', 'Price')


        # Creating a columns name heading for the table
        self._treeview.heading('Trip_ID', text = "Trip ID")
        self._treeview.column('#0', width = 0)        # root element of the treeview is set to zero width
        self._treeview.heading('Carrier', text = "Carrier")
        self._treeview.heading('Date', text = "Date")
        self._treeview.heading('Depart_Time', text = "Depart Time")
        self._treeview.heading('Arrive_Time', text = "Arrive Time")
        self._treeview.heading('From', text = "From")
        self._treeview.heading('To', text = "To")
        self._treeview.heading('#_of_Transfer', text = "# of Transfer")
        self._treeview.heading('Price', text = "$ Price")


        # The column size is 100
        for item in self._treeview['columns']:
            self._treeview.column(item, width = 100)

        self._treeview.pack()



    # when exit button is clicked, the GUI frame close
    def _exit(self):
        sys.exit()



    # when the search button is clicked, use this function
    def _search(self):

        # delete every data from the table and inserting updated data to the table
        for item in self._treeview.get_children():
            self._treeview.delete(item)


        db = sqlite3.connect(database_filename)

        # get user input and put in a variable
        BusDate = self.BusDateVar.get()
        BusTime = self.BusTimeVar.get()

        # parsing the user input so that user can put any format of Date and Time
        Bus_Date = parser.parse(BusDate)
        Bus_Time = parser.parse(BusTime)

        cursor = db.cursor()
        cursor.execute('SELECT * FROM busTable;')

        # checking to see if the data is in the busTable
        itemsDB = cursor.fetchall()
        print(itemsDB)


        db.close()


        # inserting the bus trip data to a treeview table,
        # where bus trip date is equal to user input and bus trip depart time user input is equal or later time
        for row in itemsDB:
            if parser.parse(row[2])==Bus_Date and parser.parse(row[3])>=Bus_Time:
                self._treeview.insert('', 'end', values = row)




# Creating a table called " busTable " and inserting a data into busTable table
def setup_database():

    global db, cursor, rows
    db = sqlite3.connect(database_filename)
    cursor = db.cursor()

    # Create a database table called " busTable " with a column name with a data type they use in column
    cursor.execute('CREATE TABLE if NOT EXISTS busTable (tripID Integer, carrier text, date text,'
                   ' departTime text, arriveTime text, fromLocation text, toLocation text, transfer Integer,'
                   ' price text)')


    # commit saves changes
    db.commit()

    # close the connection to the database.
    db.close()

    start_gui()



# Display GUI Frame
def start_gui():

    hyGUI().mainloop()



# Calling to set up basic database table and start to make GUI frame
def main():
    setup_database()
    start_gui()


if __name__ == '__main__':
    main()










