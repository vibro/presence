#!/usr/local/bin/python2.7


''' This module consists of Presence helper functions to view events in the database.
 May be merged with other modules later. 

Created by Lulu Ye - May 2014'''


import MySQLdb
from rugsbee_dsn import DSN 
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global

''' Called on submit '''
def submit(form_data):
#    print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #retrieves the data from the form for the sql query
    view = form_data.getfirst("view") #whether in team or user mode
    id = form_data.getfirst("ID")
    
    # print "view: " + view +", " + id #debugging ometimes doesn't work if id is empty
    return getEvent(id,view)


# Fetches the events of a given team
def getEvent(id,view):
    global curs
    
    print "right outside of checking for view" #debugging
    #user event query
    if (view == "user"):
        # print "hello! Querying for user events for id No. " + id #debugging

        # actually might be more complicated since we want the events - double check that this is working, because it is not
        curs.execute('SELECT * FROM event,(SELECT * FROM attend WHERE UID = 1) as userEv where userEv.EID = event.EID', (id,))
    else:
    #team event query
        curs.execute('SELECT * FROM event WHERE host_id = %s', (id,))
    
    lines=[]
    
    while True:
        row = curs.fetchone()
        # print "curs.fetchone: " #debugging
        print row #debugging
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return "<h2> Events </h2> \n <ul>" + "\n".join(lines) + "\n </ul>"
        lines.append('<li> ' + row.get('location'))
        # print lines #debugging
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
