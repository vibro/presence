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
    #print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #retrieves the data from the form for the sql query
    view = form_data.getfirst("view") #whether in team or user mode
    id = form_data.getfirst("ID")
    
    # print "view: " + view +", " + id #debugging ometimes doesn't work if id is empty
    return getEvent(str(id),view)


# Fetches the events of a given team
def getEvent(id,view):
    global curs
    
    #print "<p> right outside of checking for view: " #debugging
    #print view #debugging
    #user event query
    if (view == "user"):
        #print "<p>hello! Querying for user events for id No. " + id #debugging
        curs.execute('SELECT * FROM event,(SELECT * FROM attend WHERE UID = %s) as userEv where userEv.EID = event.EID', (id,))

    else:
    #team event query - set as default
        curs.execute('SELECT * FROM event WHERE host_id = %s', (id,))


    # HTML Formatting below 
    header = "<div class=\"container\"><h2> Events for " + view + " no. " + str(id) +  "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> host_id </th> \n <th> location </th> \n </tr>"
    tableEnd = "</table></div>"

    lines = []
    
    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        '''Advanced functionality of this would include using JSON to provide a sortable view of the events. We can implement this
        In the future.'''
        
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('host_id')) + "</td>")
        lines.append("<td>" + row.get('location') + "</td>" + "</tr>")
        # print lines #debugging
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
