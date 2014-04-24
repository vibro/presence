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
    name = form_data.getfirst("teamName") #needs escape
    location = form_data.getfirst("location") #needs escape
    

    createTeam(manager,name,location)
    
    
''' Creates a team by executing a SQL insert statement.'''
def createTeam(manager,name,loc):
    global curs
    curs.execute('INSERT INTO team(manager,name, location) VALUES(%s,%s,%s)',(manager, name, loc))
    
    if (name != None):
        print ("<p>Your team <em>" + name + "</em> has been created")
        

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db'
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
