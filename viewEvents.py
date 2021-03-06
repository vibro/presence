#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to view events in the database.
May be merged with other modules later. 

Created by Lulu Ye - May 2014'''
#TODO: be able to view one team's events from a user standpoint
# ie, only show team 1 but allow user to update attendance


import cgi
import cgi_utils_sda
import session


''' Called on submit '''
def submit(form_data,submit_type): 
    #need a different submit_type so that it executes the right code
    #print "submit method in createTeam.py"
    #connect to the database
        
    if (submit_type == "Update Attendance"):
        #retrieves the data from the form to update the database
        return updateAttendance(form_data)
        #execute Attendance thing
    elif (submit_type == "View Attendance"):
        return printAttendance(form_data) # Needs to retrieve the proper information in the data
    else:
    #retrieves the data from the form for the sql query for events
        view = form_data.getfirst("view") #whether in team or user mode
        TID = session.getTeamFromSession()
        UID = session.getUserFromSession()
    
    # print "view: " + view +", " + id #debugging ometimes doesn't work if id is empty
        return getEvent(str(TID),str(UID),view)
    
# Fetches the events of a given team
def getEvent(TID,UID,view):
    curs = session.cursor(session.connect())
    #print "<p> right outside of checking for view: " #debugging
    #print view #debugging
    #user event query
    if (view == "team"):
        return printTeamTable(TID)
    elif (view == "user"):
        return printUserTable(UID)
    elif (view == "userteam"):
        return printUserTeamTable(UID,TID)
    else:
        return ""


''' Prints the table data cell of the radio button.
 requires the EID, the UID, and the status of the user
'''
def printAttendRadio(user,event,check):    
# depending on what was in the database, the appropriate radio will be checked.
    yes ="<input type=\"radio\" name=\"attend\" value=\"yes\""
    no = "<input type=\"radio\" name=\"attend\" value=\"no\""
    maybe ="<input type=\"radio\" name=\"attend\" value=\"maybe\""
    if (check == "n"):
        no += " checked"
    elif (check == "m"):
        maybe += " checked"
    else:
        yes += " checked"
        
    yes += "> <label class=\"radio\"> Yes</label>\n" #yes option
    no += "> <label class=\"radio\"> No</label>\n" #no option
    maybe += "> <label class=\"radio\"> Maybe</label>\n" #maybe option"
    
    formhead = "<td><form method=\"post\" action=\"viewEvents.cgi\" class=\"form-inline\">" # runs the viewEvents.cgi
    
    html ="<input type=\"submit\" name=\"submit\" value=\"Update Attendance\" class=\"btn\"> \n" #submit button
    html +="<input type=\"hidden\" name=\"event\" value=\""+ event + "\">\n" #encodes the event type
    html +="<input type=\"hidden\" name=\"user\" value=\"" + user + "\">\n" #encodes the userID. Might not need this later with sessions

    #hidden value for the event id, always returns 1 at this point
    # Also add a comment box later
    html +="</form></td>"
    return formhead + yes + no + maybe + html

#returns the users attending an event
def printAttendance(form_data):
    EID = form_data.getfirst("event")

    curs = session.cursor(session.connect())
    curs.execute('SELECT * from attend where EID = %s', (EID,)) #Make this so it generates the name

    response = "<br>Event Name <br> <table class='table table-striped'> <tr><thead> <th> User ID </th> <th> Attend? </th> </thead> </tr>"

    while True:
        row = curs.fetchone()
        if row == None:
            return response
        response += "<tr><td>UID: " + str(row.get("UID")) + "</td><td> status: " + str(row.get("status")) + "</td></tr>"

# HTML method. Print the form and the table header for the user
def printUserTable(id):
    curs = session.cursor(session.connect())
    #execute the SQL query
    curs.execute('SELECT * FROM (SELECT event.EID, host_id, location, event_date, event_name, status FROM event,(SELECT * FROM attend WHERE UID = %s) as userEv where userEv.EID = event.EID) as ev, team where ev.host_id = TID', (id,))

    
    # HTML Formatting below 
    header = "<div class=\"panel panel-default\"><div class='panel-heading'> Events for User no. " + str(id) +  "</div>"
    tableHead = "<table class=\"table table-striped\"> <thead> <tr> \n <th> Team Name </th> \n <th> Location </th> \n <th> Event Date </th> \n <th> Attend?</th> </tr> </thead>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()


        '''Advanced functionality of this would include using JSON to 
        provide a sortable view of the events. We can implement this
        in the future.'''

        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd

        lines.append("<tr>" + "<td>" +  str(row.get('name')) + "</td>") #displays the hosting team
        lines.append("<td>" + str(row.get('location')) + "</td>") #displays the event location
        lines.append("<td>" + str(row.get('event_date')) + "</td>") #displays the event date
        lines.append(printAttendRadio(id,str(row.get('EID')),str(row.get('status'))) + "</td></tr>\n") 
        

# HTML method Prints the form and the table header for the team table.
def printTeamTable(id):
    curs = session.cursor(session.connect())
    #execute the SQL query that retrieves the events associated with the team
    curs.execute('SELECT * FROM event, team WHERE host_id = %s and TID = %s', (id, id))
    
        # HTML Formatting below 
    header = "<div class=\"panel panel-default\"><div class='panel-heading'> Events for Team no. " + str(id) +  "</div>"
    tableHead = "<table class=\"table table-striped\"> <thead> <tr> \n <th> Team Name </th> \n <th> Location </th> \n <th> Event Date </th> \n <th> </th> </tr> </thead>"
    tableEnd = "</table></div>"

    lines = []    

    while True:

        row = curs.fetchone() 
        print "<p>curs.fetchone: " #debugging
        print row #debugging
        
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd

        lines.append("<tr>" + "<td>" +  str(row.get('name')) + "</td>") #displays the hosting team
        lines.append("<td>" + str(row.get('location')) + "</td>") #displays the event location
        lines.append("<td>" + str(row.get('event_date')) + "</td>") #displays the event date
        lines.append("<td><form method=\"post\" action=\"viewEvents.cgi\" class=\"form-inline\">")
        lines.append("<input type=\"submit\" name=\"submit\" value=\"View Attendance\" class=\"btn\">")
        lines.append("<input type=\"hidden\" name=\"event\" value=\"" + str(row.get('EID')) + "\">\n</form></td></tr>\n") #view attending button
        #displays an optiion to view all users who are attending


def printUserTeamTable(UID,TID):
    curs = session.cursor(session.connect())
    #execute the SQL query that retrieves the events associated with the team
    curs.execute('SELECT * FROM event, team WHERE host_id = %s and TID = %s', (TID,TID))

 
    # HTML Formatting below 
    header = "<div class=\"panel panel-default\"><div class='panel-heading'> Events for team" + str(id) +  "</div>"
    tableHead = "<table class=\"table table-striped\"> <thead> <tr> \n <th> Team Name </th> \n <th> Location </th> \n <th> Event Date </th> \n <th> Attend?</th> </tr> </thead>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()


        '''Advanced functionality of this would include using JSON to 
        provide a sortable view of the events. We can implement this
        in the future.'''

        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd

        lines.append("<tr>" + "<td>" +  str(row.get('name')) + "</td>") #displays the hosting team
        lines.append("<td>" + str(row.get('location')) + "</td>") #displays the event location
        lines.append("<td>" + str(row.get('event_date')) + "</td>") #displays the event date
        lines.append(printAttendRadio(UID,str(row.get('EID')),str(row.get('status'))) + "</td></tr>\n") 
    

# Updates the attendance for only one event
def updateAttendance(form_data):
    response = form_data.getfirst("attend")
    UID = form_data.getfirst("user") #gets the userID, later might not be needed because of sessions
    EID = form_data.getfirst("event") #gets the eventID for updating database

   # print "EID" + str(EID) #debugging
   # print "UID" + str(UID) #debugging

    curs = session.cursor(session.connect())
    msg ="<div class='alert alert-success'>Attendance successfuly changed. "
    if (response == "yes"):
        msg += " You are attending to event number " + EID
#insert into the attend table that the user is attending the event
        curs.execute('UPDATE attend SET status = \'y\' where EID = %s and UID = %s', (EID,UID))
        
        #execute a sql query
    if (response == "no"):
        msg += " You are not attending event number " + EID
        curs.execute('UPDATE attend SET status = \'n\' where EID = %s and UID = %s', (EID,UID))

    if (response == "maybe"):
        msg += " You may be present."
        curs.execute('UPDATE attend SET status = \'m\' where EID = %s and UID = %s', (EID,UID))
    return msg + "</div>"
            #do nothing
    # if yes, then add the event and the user to the attends table
    # if no, then delete the event and the user from the table
        
