import sys
import MySQLdb
from rugsbee_dsn import DSN # change later
import dbconn
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import session
import Cookie

def isManager(UID,TID):
    curs = cursor(connect())
    curs.execute('SELECT TID from team where manager=%s AND TID=%s',(UID,TID))

    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True

def isCoach(UID,TID):
    curs = cursor(connect())
    curs.execute('SELECT team from coach where CID=%s AND team=%s',(UID,TID))
    
    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True

def isMember(UID,TID):
    curs = cursor(connect())
    curs.execute('SELECT PID from player where PID=%s AND team=%s',(UID,TID))

    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db' #change later to rugsbee
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn

def cursor(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs
