#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Created by Tori Brown - 21 April 2014'''


import MySQLdb
from rugsbee_dsn import DSN # change later
import dbconn
import cgi
import cgi_utils_sda
import session

''' Called on submit '''
def submit(form_data):
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

        # Retrieve and escape the necessary data to insert into the database
    password = cgi.escape(str(form_data.getfirst("password")))
    passcheck = cgi.escape(str(form_data.getfirst("passcheck")))
    
    if (password == None or passcheck == None):
        return "" #returns blank if there is no form data
    elif (password != passcheck):
        return "<div class='alert alert-danger'> Passwords do not match </div>"
    else:
        return updatePass(password)        
        
    
''' Creates an account by executing a SQL insert statement.'''
def updatePass(password):
    curs = cursor(connect())
    UID = session.getUserFromSession()
    curs.execute('UPDATE userpass set password=password(%s) where id=%s',(password,UID))
    return "<div class='alert alert-success'>Pasword successfully updated!</div>"
''' Checks if user exists by email address.'''
''' No two users can have the same email'''

def existsUser(email):
    global curs
    curs.execute('Select UID from user where email=%s',(email,))
    row = curs.fetchone()
    if row == None:
        return False
    else: return True

def existsTeam(team):
    global curs
    curs.execute('Select TID from team where TID=%s',(team,))
    row = curs.fetchone()
    if row == None:
        return False
    else: return True

def retrieveUser(UID):
    global curs
    curs.execute(('Select UID,email,name,dob,phnum,nickname ' 
                 +'from user where UID=%s'),(UID,))
    row = curs.fetchone()
    if row == None:
        print("<p> The data was not inserted correctly")
    else:
        line = ("<p>Inserted into the database was this user: \n "+
                "<li>UID: {UID} \n"+
               "<li>email: {email} \n"+
                "<li>name: {name} \n"+
                "<li>dob: {dob} \n"+
                "<li>phnum: {phnum} \n"+
                "<li>nickname: {nickname} \n").format(**row)
        print line
    curs.execute(('SELECT password from userpass where id=%s'),(UID,))
    row2 = curs.fetchone()
    if row2 == None:
        print("<p> The password was not added correctly")
    else:
        line2 = ("<p>The password for this account is: {password}").format(**row2)
        print line2


    

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db' #change later to rugsbee
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn

def cursor(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs