#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Currently connected to hye database due to some tabular differences between my tables and rugsbee

Created by Lulu Ye - April 2014'''


import MySQLdb
from rugsbee_dsn import DSN #change later to rugsbee_dsn
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global

''' Called on submit '''
def submit(form_data):
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # You'll want to insert some checks here before running the actual create event. 
    # Checks include that the information is provided and that a duplicate event doesn't exist

    # Retrieve and escape the necessary data to insert into the database
    host = form_data.getfirst("hostID")
    
    
    location = form_data.getfirst("event_loc") #needs escaping?

    date = form_data.getfirst("event_date") #refine later to date

    #put this into the date format that SQL understands
    month = form_data.getfirst("month")
    day = form_data.getfirst("day")
    year = form_data.getfirst("year")

    createEvent(host,date,location)
    
    
''' Creates an event by executing a SQL insert statement.'''
def createEvent(host,date,location):
    global curs
    curs.execute('INSERT INTO event(host_id, event_date, location) VALUES(%s,%s,%s)',(host,date,location)) #refine later
    if (date != None and location != None):
        print ("<p>Your event on " + date + " at " + location + " has been created")


''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db' #change later to rugsbee_db
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
