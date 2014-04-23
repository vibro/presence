#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Currently connected to hye database due to some tabular differences between my tables and rugsbee

Created by Lulu Ye - 21 April 2014'''


import MySQLdb
from hye_db import DSN #change later to rugsbee_dsn
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
    date = form_data.getfirst("event_date") #refine later to date
    location = cgi.escape(form_data.getfirst("event_loc")) #needs escaping?

    createEvent(host,date,location)
    
    
''' Creates an event by executing a SQL insert statement.'''
def createEvent(host,date,location):
    global curs
    curs.execute('INSERT INTO event(host_id, event_date, location) VALUES(%s,%s,%s)',(host,date,location)) #refine later
    print ("<p>Your event on " + date + " at " + location + " has been created")


''' Creates a database connection. '''
def connect():
    DSN['database']= 'hye_db' #change later to rugsbee_db
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
