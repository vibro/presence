#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Created by Tori Brown - 21 April 2014'''


import MySQLdb
from vbrown_dsn import DSN # change later
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global

''' Called on submit '''
def submit(form_data):
    print "submit method in createAccount.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    name = form_data.getfirst("name")
    dob = form_data.getfirst("dob")
    email = form_data.getfirst("email")
    phnum = form_data.getfirst("phum")
    nickname = form_data.getfirst("nickname")
    password = form_data.getfirst("pass")
    passcheck = form_data.getfirst("passcheck")
    
    if (password != passcheck):
        print("<p>Passwords do not match")
    else:
        createAccount(name,dob,email,phnum,nickname,password)
        
    
''' Creates an account by executing a SQL insert statement.'''

def createAccount(name,dob,email,phnum,nickname,password):
    global curs
    curs.execute('INSERT INTO user values(%s, %s, %s, %s, %s)', (email,name,dob,phnum,nickname))
    curs.execute('SELECT UID from user where email=%s', (email,))
    row = curs.fetchone()
    if row == None:
        print("<p>Something is wrong")
    else:
        #add the password
        uid = row['uid']
        curs.execute('INSERT into userpass values(%s, %s)',(uid,password))
        print("<p>Inserted user and password!")
        
    print ("<p>Your account has been created")


''' Creates a database connection. '''
def connect():
    DSN['database']= 'vbrown_db' #change later to rugsbee
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn
