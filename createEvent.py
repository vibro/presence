#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Created by Lulu Ye - 21 April 2014'''


import MySQLdb
from lu_db import DSN # change later, right now edited the .sql file to have more
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global

''' Called on submit '''
def submit(form_data):
    print "submit method in createEvent.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    host = form_data.getfirst("hostID")
    date = form_data.getfirst("event_date")
    location = form_data.getfirst("event_loc") #needs escaping?

    createEvent(host,date,location)
    
    
''' Creates an event by executing a SQL insert statement.'''
def createEvent(host,date,location):
    global curs
    curs.execute('INSERT INTO event(location) VALUES(%s)',(location,)) #arrrrrrrrrrrgh not working
    print ("<p>Your event has been created")


''' Creates a database connection. '''
def connect():
    DSN['database']= 'hye_db' #change later to rugsbee
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
