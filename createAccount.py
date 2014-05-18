#!/usr/local/bin/python2.7

''' This module consists of Presence helper functions to create an event.
 May be merged with other modules later. 

Created by Tori Brown - 21 April 2014'''


import MySQLdb
from rugsbee_dsn import DSN # change later
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
    name = cgi.escape(str(form_data.getfirst("name")))
    dob = str(form_data.getfirst("dob"))
    email = cgi.escape(str(form_data.getfirst("email")))
    phnum = str(form_data.getfirst("phnum"))
    nickname = cgi.escape(str(form_data.getfirst("nickname")))
    password = cgi.escape(str(form_data.getfirst("pass")))
    passcheck = cgi.escape(str(form_data.getfirst("passcheck")))
    
    if (password != passcheck):
        return "<div class='alert alert-danger'>Passwords do not match! </div>"
    elif (password != None):
        createAccount(name,dob,email,phnum,nickname,password)
        return "trying to create account" #debugging
        
        
    
''' Creates an account by executing a SQL insert statement.'''

def createAccount(name,dob,email,phnum,nickname,password):
    print "top of the createAccount method"
    global curs
    if existsUser(email):
        print "user already exists" #debugging
        return "<div class='alert alert-danger'> Account with this email already exists </div>)"
    else:
        print "inserting account" #debugging
        curs.execute('INSERT INTO user(email,name,dob,phnum,nickname) values(%s, %s, %s, %s, %s)', (email,name,dob,phnum,nickname))

        statement = "password('"+password+"')"

        print statement
        # Modifications
        curs.execute('SELECT LAST_INSERT_ID()')
        uid = curs.fetchone().get("LAST_INSERT_ID()")

        curs.execute('INSERT into userpass values(%s, %s)',(uid,statement))
        
        print("<p>Inserted user and password!")
        print ("<p>Your account has been created")
        retrieveUser(uid)  

        return "<div class='alert alert-success'> Your account has been created! </div>"
        # curs.execute('SELECT UID from user where email=%s', (email,))
        # row = curs.fetchone()
        # if row == None:
        #     print("<p>Something is wrong")
        # else:
        # #add the password
        #     uid = row['UID']
        #     curs.execute('INSERT into userpass values(%s, %s)',(uid,password))
        #     print("<p>Inserted user and password!")
        #     print ("<p>Your account has been created")
        #     retrieveUser(uid)  

''' Checks if user exists by email address.'''
''' No two users can have the same email'''

def existsUser(email):
    global curs
    curs.execute('Select UID from user where email=%s',(email,))
    row = curs.fetchone()
    print row
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
