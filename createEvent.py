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

    # Retrieve and escape the necessary data to insert into the database
    host = str(form_data.getfirst("hostID"))
    location = cgi.escape(str(form_data.getfirst("event_loc"))) 
    name = cgi.escape(str(form_data.getfirst("event_name")))

    #put this into the date format that SQL understands
    month = form_data.getfirst("month")
    day = form_data.getfirst("day")
    year = form_data.getfirst("year")
    sql_date = str(year)+ "-" + str(month) + "-" + str(day)
        #print sql_date
        #creates the event, even if the sql_date is empty
    return createEvent(host,sql_date,name,location)
    
    
''' Creates an event by executing a SQL insert statement.'''
def createEvent(host,date,name,location):
    global curs
    
    #doesn't check whether an event is duplicated since steams may sometimes hold simultaneous events.
    curs.execute('INSERT INTO event(host_id, location, event_date, event_name) VALUES(%s,%s,%s,%s)',(host,location,date,name)) 

    # retrieves the EID of the event
    curs.execute('SELECT LAST_INSERT_ID()')
    row = curs.fetchone()
    EID = row.get('LAST_INSERT_ID()') #retrieves the newly created EID

    # Adds the event to the team's players' events list by automatically marking them as "yes"
    curs.execute('INSERT INTO attend(EID,UID,status) SELECT %s, PID, \'y\' FROM player WHERE TEAM = %s',(EID, host))
    

    if (location != "None"):
        response = "<div class='alert alert-success'>"
        response += "<p>Your event <em>" + name + "</em> on " + date + " at <em>" + location + "</em> has been created"
        response +="</div>"
    else:
        response = "<div class='alert alert-danger'> Uh oh! Something went wrong. Check your inputs again. </div>"
    return response

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db' #change later to rugsbee_db
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
