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
    id = form_data.getfirst("UID")

    if (id != None):
        return getTeam(str(id))
    else:
        return ""


# Fetches the roster of a given team and outputs results in HTML
def getTeam(id):
    global curs
    
    #Querying for the players on the team
    curs.execute('select name,TID from team inner join player where player.team=TID and PID=%s',(id,))
    

    # HTML Formatting below 
    header = "<div class=\"panel panel-default\"><div class='panel-heading'> Teams for user no. " + str(id) +  "</div>"
    tableHead = "<table class=\"table table-striped\"> <thead> <tr> \n <th> TID </th> \n <th> Team Name </th> \n </tr> </thead>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('TID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>" + "</tr>")
        # print lines #debugging
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
