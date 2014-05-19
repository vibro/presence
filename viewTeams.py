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
import dashboard
import session



''' Called on submit '''
def submit(form_data):
    #print "submit method in createTeam.py"
    #connect to the database
    
    #retrieves the data from the form for the sql query
    id = form_data.getfirst("UID")

    if (id != None):
        return getTeam(str(id))
    else:
        return ""


# Fetches the roster of a given team and outputs results in HTML
def getTeam(id):
    curs = cursor(connect())
    
    #Querying for the players on the team
    curs.execute('select name,TID from team inner join player where player.team=TID and PID=%s',(id,))
    

    # HTML Formatting below 

    header = "<div class=\"container\"><h2> Teams for user with ID:" + str(id) + "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> TID </th> \n <th> Team Name </th> \n <th> </th> \n </tr>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
        TID = str(row['TID'])
        status = checkTeam(TID)
        # TODO: Implement JS so that TID is set in session table
        # When proper link is clicked
        lines.append("<tr>" + "<td>" +  str(row.get('TID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>")
        if (status == "manager") or (status == "coach"):
            lines.append("<td>" + "<a href='dashboard.cgi?TID="+TID+"'>Manage Team</a>" + "</td>" + "</tr>")
        elif (status == "player"):
            lines.append("<td>" + "<a href='dashboard.cgi?TID="+TID+"'>View Team</a>" + "</td>" + "</tr>")
           
        # print lines #debugging
    
    

def checkTeam(TID):
    UID = session.getUserFromSession()
    if (dashboard.isManager(UID,TID)):
        return "manager"
    elif (dashboard.isCoach(UID,TID)):
        return "coach"
    elif (dashboard.isMember(UID,TID)):
        return "player"
    else:
        return ""




''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn

def cursor(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs

