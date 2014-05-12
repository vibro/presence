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
def submit(form_data,submit_type): 
    #need a different submit_type so that it executes the right code
    #print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    if (submit_type == "Update Attendance"):
        return updateAttendance("yes") #for now just maybe
        #execute Attendance thing
    else:
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
    if (view is None):
        return ""
    elif (view == "user"):
        #print "<p>hello! Querying for user events for id No. " + id #debugging
        curs.execute('SELECT * FROM event,(SELECT * FROM attend WHERE UID = %s) as userEv where userEv.EID = event.EID', (id,))

    else:
    #team event query - set as default
        curs.execute('SELECT * FROM event WHERE host_id = %s', (id,))

        # HTML Formatting below 
    header = "<div class=\"container\"><h2> Events for " + str(view) + " no. " + str(id) +  "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> host_id </th> \n <th> location </th> \n <th> event_date </th> \n <th> Attend</th> </tr>"
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
                
        # Later, perhaps modularize this to print out multiple rows of data
        lines.append("<tr>" + "<td>" +  str(row.get('host_id')) + "</td>")
        lines.append("<td>" + str(row.get('location')) + "</td>")
        lines.append("<td>" + str(row.get('event_date')) + "</td>")
        lines.append(printAttendRadio())
        # lines.append("<td><form> <input type=\"radio\" name=\"attend\" value=\"yes\"> yes </form> </td> </tr>")
        # print lines #debugging


def printHtmlRow(host, loc, date):
    html = ""
    # fill this in later
    return html

#prints the table data cell of the radio button
def printAttendRadio(): 
    html = "<td><form method=\"post\" action=\"viewEvents.cgi\">" # runs the viewEvents.cgi
    html +="<input type=\"radio\" name=\"attend\" value=\"yes\" checked> yes" #yes option
    html += "<input type=\"radio\" name=\"attend\" value=\"no\"> no" #no option
    html +="<input type=\"radio\" name=\"attend\" value=\"maybe\"> maybe" #maybe option
    html +="<input type=\"submit\" name=\"submit\" value=\"Update Attendance\"> " #submit button
    # Also add a comment box later
    html +="</form></td>"
    return html

def updateAttendance(response):
    global curs
    msg =""
    if (response == "yes"):
        msg = "<p>yes, I'm coming!"
        
        #execute a sql query
    if (response == "no"):
        msg = "<p>no, I'm busy"
    
    return msg + "<p>end of updateAttendance"
            #do nothing
    # if yes, then add the event and the user to the attends table
    # if no, then delete the event and the user from the table
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
