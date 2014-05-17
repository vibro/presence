import MySQLdb
from rugsbee_dsn import DSN # change later
import dbconn
import cgi
import cgi_utils_sda

def submitLogin(form_data,sessid):
    email = form_data.getfirst('email')
    password = form_data.getfirst('password')
    error = False
    UID = ""
    if (email is not None or password is not None):
        UID = getUID(email)
        error = checkPass(UID,password)

    return error,UID
    
def setUserSession(sessid,uid):
    curs = cursor(connect())
    if existsSession(sessid):
        print "session exists"
        return "already logged in"
    else:
        curs.execute('INSERT INTO session(SESSID,UID) values(%s,%s)',(sessid,uid))
        return "Successfully logged in"

def deleteSession(sessid):
    curs = cursor(connect())
    curs.execute('DELETE from session where SESSID=%s',(sessid,))

def existsSession(sessid):
    curs = cursor(connect())
    curs.execute('SELECT SESSID from session where SESSID=%s',(sessid,))
    row = curs.fetchone()
    if row == None:
        return False
    else: 
        return True

def getUID(email):
    curs = cursor(connect())
    curs.execute('SELECT UID from user where email=%s',(email,))
    row = curs.fetchone()
    if row == None:
        return None
    else:
        UID = row['UID']
        return UID

def getUser(sessid):
    curs = cursor(connect())
    curs.execute('SELECT UID from session where SESSID=%s',(sessid,))
    
    row = curs.fetchone()
    if row == None:
        return None
    else:
        uid = row['UID']
        return str(uid)

def getUserFromSession():
    cookie = cgi_utils_sda.getCookieFromRequest("SESSID")
    UID = getUser(str(cookie.value))
    return UID

def checkPass(uid,password):
    curs = cursor(connect())
    curs.execute('SELECT * from userpass where id=%s',(uid,))
    row = curs.fetchone()
    if row != None:
        
        uid = row['id']
        origpass = row['password']
        #print "orig pass: "+ origpass +"\n"
    curs.execute('SELECT password(%s)',(password,))
    row = curs.fetchone()
    if row == None:
        #print 'wrong password'
        passcheck = None
    else:
        passcheck = row["password('"+password+"')"]
        #print "passcheck: "+ passcheck
    if (passcheck == origpass):
        #print "success! you are now logged in!"
        return True
    else:
        #print "password incorrect"
        return False

''' Creates a database connection. '''
def connect():
    DSN['database']= 'rugsbee_db' #change later to rugsbee
    conn = dbconn.connect(DSN)
    conn.autocommit(True)
    return conn

def cursor(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs
