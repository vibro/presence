#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Created by Tori Brown - 21 April 2014'''

import cgi
import cgi_utils_sda
import session

''' Called on submit '''
def submit(form_data):
    
    
    # Retrieve and escape the necessary data to insert into the database
    name = cgi.escape(str(form_data.getfirst("name")))
    location = cgi.escape(str(form_data.getfirst("locationx")))
    
    if (location != None):
        return updateLocation(location) #returns blank if there is no form data
    elif (name != None):
        return updateName(name)   
    else:
        return ""
 
def delete():
    TID = session.getTeamFromSession()
    curs = session.cursor(session.connect())
    curs.execute('DELETE from team where TID=%s',(TID,))
    curs.execute('DELETE from player where team=%s',(TID,))
    curs.execute('DELETE from coach where team=%s',(TID,))
    curs.execute('UPDATE session set TID=NULL where TID=%s',(TID))
    
    line = "<div class='alert alert-danger'> Team deleted \t <a href='userDashboard.cgi'>Return to Dashboard</a></div>"
    return line
    
''' Creates an account by executing a SQL insert statement.'''
def updateLocation(location):
    curs = session.cursor(session.connect())
    TID = session.getTeamFromSession()
    curs.execute('UPDATE team set location=%s where TID=%s',(location,TID))
    return "<div class='alert alert-success'>Location successfully updated!</div>"

def updateName(name):
    curs = session.cursor(session.connect())
    TID = session.getTeamFromSession()
    curs.execute('UPDATE team set name=%s where TID=%s',(name,TID))
    return "<div class='alert alert-success'>Team name successfully updated!</div>"

