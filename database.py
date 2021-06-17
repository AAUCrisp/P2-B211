import pyautogui        #screenshot library
import sqlite3 as lite  #importing sqlite (database)
import sys              #importing module that gives access to computer system
import os, shutil       #importing os module that allows us to use operating system dependent functionality
                        #importing shutil that allows file copying and/or removing. 
import datetime
import os.path                #importing pathname manipulations
import time                   #importing time module so we can make the programme sleep for a certain amount of secs.
import glob                   #importing glob module

#creating project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create a version of the database in database file (.db)
DB_NAME = "screenshotDatabase.db"

# Method to take the screenshot and insert the filename and path into the database
def takeScreenshot():
    timestamp = datetime.datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d-%H-%M-%S")
    newScreenshot = pyautogui.screenshot()

    #determining path the screenshot will be saved to (a) specified foler path in Python folder/explorer)
    saveScreenshot = f"{ROOT_DIR}\Screenshots\Screenshot{timestamp_str}.PNG"

    #saving the screenshot in given folder
    newScreenshot.save(saveScreenshot)

    print("Screenshot has been saved!")

   
#  ---  Function to insert file information in database  --- 

def dbFileInsert(tableName, filePath):            ##  Can easily be rewritten into universal "insertIntoDB()" thingy-ma-ding, but don't wanna change too much right now
    #Create SQL string
    sql = """ 
        INSERT INTO """ + tableName + """ VALUES('""" + filePath + """'); 
        """
    # Send statement to the Database.
    updateDB(sql)


#  ---  Function to create a database table  ---       takes and string array in the column parameter, including the datatype    ex. "name TEXT"
def createTable(tableName, columns):
    # Start creating SQL string with the tablename
    sql = """
        DROP TABLE IF EXISTS """ + tableName + """; 
        CREATE TABLE """ + tableName + """ ("""

    # Loop over the columns and insert them into the SQL string
    for i in range(len(columns)):
        if i > 0:           # If this isn't the first iteration
            sql += """, """  # Insert a comma to separate them
        sql += columns[i]   # Insert column name into string

    sql += """);""" # Finish up the SQL string
    
    # Send statement to the database.
    updateDB(sql)



#  ---  Function to send update querys to the database  ---
def updateDB(sql):
    print(sql)  # Write out the statement, just for testing purposes
    # Connect to the database
    con = lite.connect(DB_NAME)
    # Creates the SQLite cursor that is used to query the database
    cur = con.cursor()
    #Executing the desired database script
    cur.executescript(sql)
    # Force the database to make changes with the commit command
    con.commit()
    # Close the database
    con.close()


#  ---  Function to fetch all from a table  ---
def listAll(tableName):
    sql = 'SELECT * FROM ' + tableName

    # Connect to the database
    con = lite.connect(DB_NAME)
    # Creates the SQLite cursor that is used to query the database
    cur = con.cursor()
    # Execute simple SQL query
    cur.execute(sql)

    # Loop over the returned data and write it out in the console
    for i in cur:
        print("\n")
        for j in i:
            print(j)

    # Close the database
    con.close()


### Creating a way to store the path for the images in the database"
def screenshots():

    #calling function that takes screenshot and saves it in a folder on users computer
    takeScreenshot()

    #making a list array of all screenshots in the folder on the Python folder - shortcut for listdir + fnmatch
    allScreenshots = glob.glob(f"{ROOT_DIR}\Screenshots\*.png")
    

    #getting the total length of the list array
    amountScreenshots = len(allScreenshots)

    #if statement: if array place is over 0, take last place in array
    if amountScreenshots > 0:
        lastScreenshot = allScreenshots[amountScreenshots - 1]
        print(lastScreenshot)
   
   #creating variable that replaces the root directionary with empty string, so file path is dymnamic
    dbPath = lastScreenshot.replace(ROOT_DIR,"")

    #calling the function that inserts filepath into database with table name Screenshots and file path specificied with function dbPath
    dbFileInsert("Screenshots",dbPath)
    