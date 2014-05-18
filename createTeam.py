#!/usr/local/bin/python2.7

# Do you see me?

''' This module consists of Presence helper functions to insert a team into a database.
 May be merged with other modules later. 

Created by Lulu Ye - 19 April 2014'''


import MySQLdb
from rugsbee_dsn import DSN 
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global

''' Called on submit '''
def submit(form_data):
#    print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    manager = form_data.getfirst("teamManager")
    name = cgi.escape(str(form_data.getfirst("teamName")))
    location = cgi.escape(str(form_data.getfirst("location"))) 

    return createTeam(manager,name,location)
    
    
''' Creates a team by executing a SQL insert statement.'''
def createTeam(manager,name,loc):
    global curs
    curs.execute('INSERT INTO team(manager,name, location) VALUES(%s,%s,%s)',(manager, name, loc))
    
    if (name != None):
        return "<div class='alert alert-success'>Your team <em>" + name + "</em> has been created. Now you can <a href='./addMember.cgi'>add some members</a>!</div>"
    else:
        return "<div class='alert alert-danger'> Uh oh! Something went wrong when creating your team. Double check your inputs!</div>"
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
