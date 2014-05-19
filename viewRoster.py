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
import session

''' Called on submit '''
def submit():
    #print "submit method in createTeam.py"
    #connect to the database
    

    #retrieves the data from the form for the sql query
    TID = session.getTeamFromSession()
    
    if (TID != None):    
        return getRoster(str(TID))
    else:
        return ""


# Fetches the events of a given team and prints them in a striped table
def getRoster(id):
    curs = session.cursor(session.connect())
    name = session.getTeamName()
    
    curs.execute('select name,PID from player inner join user where PID=UID and team=%s',(id,))
    

   
    header = "<div class=\"panel panel-default\"><div class='panel-heading'> Roster for team " + str(name) +  "</div>"
    tableHead = "<table class=\"table table-striped\"> <thead><tr> \n <th> PID </th> \n <th> Player Name </th> \n </tr></thead>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        
        if row == None:
        
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('PID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>" + "</tr>")
       
        
