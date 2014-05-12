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
            
        #retrieves the data from the form to update the database
        return updateAttendance(form_data) #for now just maybe
        #execute Attendance thing
    else:
    #retrieves the data from the form for the sql query for events
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
        #printUserTable

    else:
    #team event query - currently set as default
        curs.execute('SELECT * FROM event WHERE host_id = %s', (id,))
        #printTeamTable

    ''' We need to differentiate between the user and the team tables.
    The user table will include an option to attend an event, and the team
    will have the option of viewing the eventss.'''


        # HTML Formatting below 
    header = "<div class=\"container\"><h2> Events for " + str(view) + " no. " + str(id) +  "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> host_id </th> \n <th> location </th> \n <th> event_date </th> \n <th> Attend</th> </tr>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        '''Advanced functionality of this would include using JSON to 
        provide a sortable view of the events. We can implement this
        in the future.'''
        
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
                
        # Later, perhaps modularize this to print out multiple rows of data
        lines.append("<tr>" + "<td>" +  str(row.get('host_id')) + "</td>")
        lines.append("<td>" + str(row.get('location')) + "</td>")
        lines.append("<td>" + str(row.get('event_date')) + "</td>")
        lines.append(printAttendRadio(id,str(row.get('EID')))) #user--assuming that this is only for the user, #event
        # lines.append("<td><form> <input type=\"radio\" name=\"attend\" value=\"yes\"> yes </form> </td> </tr>")
        # print lines #debugging


def printHtmlRow(host, loc, date):
    html = ""
    # fill this in later
    return html

#prints the table data cell of the radio button.
# requires the EID and the UID for the user
def printAttendRadio(user,event): 
    html = "<td><form method=\"post\" action=\"viewEvents.cgi\">" # runs the viewEvents.cgi
    html +="<input type=\"radio\" name=\"attend\" value=\"yes\" checked> yes\n" #yes option
    html += "<input type=\"radio\" name=\"attend\" value=\"no\"> no\n" #no option
    html +="<input type=\"radio\" name=\"attend\" value=\"maybe\"> maybe\n" #maybe option
    html +="<input type=\"submit\" name=\"submit\" value=\"Update Attendance\"> \n" #submit button
    html +="<input type=\"hidden\" name=\"event\" value=\""+ event + "\">\n" #encodes the event type
    html +="<input type=\"hidden\" name=\"user\" value=\"" + user + "\">\n" #encodes the userID. Might not need this later with sessions

    #hidden value for the event id, always returns 1 at this point
    # Also add a comment box later
    html +="</form></td>"
    return html



# HTML method. Print the form and the table header for the user
def printUserTable():
    #execute the SQL query

# HTML method Prints the form and the table header for the team table.
def printTeamTable():
    #execute the SQL query



# Updates the attendance for only one event
def updateAttendance(form_data):
    ''' debugging
    print("Your attendance form contained")    
    for k in form_data:
        print("{key} => {value}".format(key=k,value=form_data.getfirst(k)))
    '''
    response = form_data.getfirst("attend")
    UID = form_data.getfirst("uid") #gets the userID, later might not be needed because of sessions
    EID = form_data.getfirst("event") #gets the eventID for updating database
    

    global curs
    msg =""
    if (response == "yes"):
        msg = "<p>yes, I'm coming to event number " + EID

#insert into the attend table that the user is attending the event
        curs.execute('INSERT INTO attend VALUES(%s, %s)', (EID,UID))
        
        #execute a sql query
    if (response == "no"):
        msg = "<p>no, I'm busy. Deleting my presence from event number " + EID
        curs.execute('DELETE FROM attend WHERE EID = %s and UID = %s', (EID,UID))
        
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
