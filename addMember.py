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
    tid = form_data.getfirst("tid")
    email = cgi.escape(str(form_data.getfirst("email")))
    type = form_data.getfirst("type")
    
    if (tid == None or email == None):
        return "<div class='alert alert-danger'>Please input proper team id or email</div>"
    else:
        return addMember(tid,email,type)
        
        
    
''' Creates an account by executing a SQL insert statement.'''

def addMember(tid,email,type):
    global curs
    if not existsUser(email):
        return "<div class='alert alert-danger'> Account with this email does not exist</div>"
        #TODO send email with invitation to application?
    elif not existsTeam(tid):
        return "<div class='alert alert-danger'> Team with that id does not exist</div>"
    else:
        curs.execute('SELECT UID from user where email=%s', (email,))
        row = curs.fetchone()
        pid = row['UID']
        if (type == "player"):
            #We should probably check to see whether this player's already on the team's roster

            #insert player into player table
            curs.execute('INSERT into player(PID,team) values(%s,%s)', 
                         (pid,tid))

            return "<div class='alert alert-success'>Added player to the team! <div>"
        elif (type == "coach"):
            #update team to have a different coach
            curs.excute('INSERT into coach(CID,team) values(%s,%s)',(pid,tid))
            return "<div class='alert alert-success'>Added coach to the team! <div>"
        elif (type == "manager"):
            curs.execute('UPDATE team set manager = %s',(pid))
            return "<div class='alert alert-success'>Manager changed for the team! <div>"

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
