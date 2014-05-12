#!/usr/local/bin/python2.7


''' This module consists of Presence helper functions to view teams in the database.
May be merged with other modules later. 

Created by Lulu Ye - May 2014
Edited to work with teams by Tori Brown'''


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
    id = form_data.getfirst("TID")
    
    
    return getRoster(str(id))


# Fetches the events of a given team
def getRoster(id):
    global curs
    
    #print "<p> right outside of checking for view: " #debugging
    #print view #debugging
    #user event query
    
    #print "<p>hello! Querying for user events for id No. " + id #debugging
    curs.execute('select name,PID from player inner join user where PID=UID and team=%s',(id,))
    

    # HTML Formatting below 
    header = "<div class=\"container\"><h2> Roster for team with ID:" + str(id) + "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> PID </th> \n <th> Player Name </th> \n </tr>"
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
        lines.append("<tr>" + "<td>" +  str(row.get('PID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>" + "</tr>")
        # print lines #debugging
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
