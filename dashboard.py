import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import session
import Cookie

def connect():
    return session.cursor(session.connect())

def isManager(UID,TID):
    curs = connect()
    curs.execute('SELECT TID from team where manager=%s AND TID=%s',(UID,TID))

    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True

def isCoach(UID,TID):
    curs = connect()
    curs.execute('SELECT team from coach where CID=%s AND team=%s',(UID,TID))
    
    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True

def isMember(UID,TID):
    curs = connect()
    curs.execute('SELECT PID from player where PID=%s AND team=%s',(UID,TID))

    row = curs.fetchone()
    if row == None:
        return False
    else:
        return True
