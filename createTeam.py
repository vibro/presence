#!/usr/local/bin/python2.7

# Do you see me?

''' This module consists of Presence helper functions to insert a team into a database.
 May be merged with other modules later. 

Created by Lulu Ye - 19 April 2014'''


import cgi
import cgi_utils_sda
import session


''' Called on submit '''
def submit(form_data):
#    print "submit method in createTeam.py"
    #connect to the database
    
    # Retrieve and escape the necessary data to insert into the database
    manager = session.getUserFromSession()
    name = cgi.escape(str(form_data.getfirst("teamName")))
    location = cgi.escape(str(form_data.getfirst("location"))) 

    if (name, location) != ("None", "None"):
        return createTeam(manager,name,location)
    else:
        return ""
    
''' Creates a team by executing a SQL insert statement.'''
def createTeam(manager,name,loc):
    curs = session.cursor(session.connect())
    curs.execute('INSERT INTO team(manager,name, location) VALUES(%s,%s,%s)',(manager, name, loc))

    curs.execute('SELECT TID from team where TID=LAST_INSERT_ID()')
    TID = curs.fetchone().get("TID")
    session.setTeam(TID)

    curs.execute('INSERT INTO player(PID,team) values(%s,%S)',(manager,TID))
    
    if (name != "None"):
        return "<div class='alert alert-success'>Your team <em>" + name + "</em> has been created. Now you can <a href='./dashboard.cgi?TID="+str(TID)+"'>manage your team</a>!</div>"
    else:
        return "<div class='alert alert-danger'> Uh oh! Something went wrong when creating your team. Double check your inputs!</div>"
