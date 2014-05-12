''' Consolidated functions for Presence
	by Lulu Ye and Tori Brown
	May 7 2014
	Merged by Tori Brown
'''


import MySQLdb
from rugsbee_dsn import DSN # change later
import dbconn
import cgi
import cgi_utils_sda

global conn #declaring global conn
global curs #declaring global


'''Imported from addMember.py'''

''' Called on submit '''
def submitAddMember(form_data):
    print "submit method in addMember.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    tid = form_data.getfirst("tid")
    email = form_data.getfirst("email")
    type = form_data.getfirst("type")
    
    if (email == None or email == None):
        print("<p>Please input proper team id or email")
    else:
        addMember(tid,email,type)
        
''' Creates an account by executing a SQL insert statement.'''

def addMember(tid,email,type):
    global curs
    if not existsUser(email):
        print("<p>Account with this email does not exist")
        #TODO send email with invitation to application?
    elif not existsTeam(tid):
        print("<p>Team with that id does not exist")
    else:
        curs.execute('SELECT UID from user where email=%s', (email,))
        row = curs.fetchone()
        pid = row['UID']
        if (type == "player"):
            #insert player into player table
            
            curs.execute('INSERT into player(PID,team) values(%s,%s)', 
                         (pid,tid))

            print("<p>Added player to the team!")
                
        elif (type == "coach"):
            #update team to have a different coach
            curs.excute('INSERT into coach(CID,team) values(%s,%s)',(pid,tid))
            print("<p>Added a coach to the team!")
        elif (type == "manager"):
            curs.execute('UPDATE team set manager = %s',(pid))
            print("<p>Manager changed for team")



'''Imported from createAccount.py'''

''' Called on submit '''
def submitCreateAccount(form_data):
    print "submit method in createAccount.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    name = form_data.getfirst("name")
    dob = form_data.getfirst("dob")
    email = form_data.getfirst("email")
    phnum = form_data.getfirst("phnum")
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
    if existsUser(email):
        print("<p>Account with this email already exists")
    else:
        curs.execute('INSERT INTO user(email,name,dob,phnum,nickname) values(%s, %s, %s, %s, %s)', (email,name,dob,phnum,nickname))

        statement = "password('"+password+"')"
        print statement
        curs.execute('INSERT into userpass values(last_insert_id(), password(%s))',(password,))
        print("<p>Inserted user and password!")
        print ("<p>Your account has been created")
        
        curs.execute('SELECT UID from user where email=%s', (email,))
        row = curs.fetchone()
        if row == None:
            print("<p>Something is wrong")
        else:
            uid = row['UID']
            retrieveUser(uid)  
          
'''Imported from createEvent.py'''

''' Called on submit '''
def submitCreateEvent(form_data):
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
    sql_date = "" #initialize to empty


    if (month != None and day != None and year != None):
        sql_date = year+ "-" + month + "-" + day
        #print sql_date
    #creates the event, even if the sql_date is empty
    createEvent(host,sql_date,location)
    
    
''' Creates an event by executing a SQL insert statement.'''
def createEvent(host,date,location):
    global curs
    curs.execute('INSERT INTO event(host_id, event_date, location) VALUES(%s,%s,%s)',(host,date,location)) #refine later
    if (date != None and location != None):
        print ("<p>Your event on " + date + " at " + location + " has been created")

''' Imported from createTeam.py '''
''' Called on submit '''
def submitCreateTeam(form_data):
#    print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve and escape the necessary data to insert into the database
    manager = form_data.getfirst("teamManager")
    name = form_data.getfirst("teamName") #needs escape
    location = form_data.getfirst("location") #needs escape
    

    createTeam(manager,name,location)
    
    
''' Creates a team by executing a SQL insert statement.'''
def createTeam(manager,name,loc):
    global curs
    curs.execute('INSERT INTO team(manager,name, location) VALUES(%s,%s,%s)',(manager, name, loc))
    
    if (name != None):
        print ("<p>Your team <em>" + name + "</em> has been created")


''' Imported from viewEvents.py '''
''' Called on submit '''
def submitViewEvents(form_data):
    #print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #retrieves the data from the form for the sql query
    view = form_data.getfirst("view") #whether in team or user mode
    id = form_data.getfirst("ID")
    
    # print "view: " + view +", " + id #debugging ometimes doesn't work if id is empty
    return getEvent(str(id),view)


# Fetches the events of a given team
def getEvent(id,view):
    global curs
    
    #user event query
    if (view == "user"):
        curs.execute('SELECT * FROM event,(SELECT * FROM attend WHERE UID = %s) as userEv where userEv.EID = event.EID', (id,))

    else:
    #team event query - set as default
        curs.execute('SELECT * FROM event WHERE host_id = %s', (id,))

        # HTML Formatting below 
    header = "<div class=\"container\"><h2> Events for " + str(view) + " no. " + str(id) +  "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> host_id </th> \n <th> location </th> \n </tr>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        '''Advanced functionality of this would include using JSON to provide a sortable view of the events. We can implement this
        In the future.'''
        
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('host_id')) + "</td>")
        lines.append("<td>" + row.get('location') + "</td>" + "</tr>")
        # print lines #debugging

''' Imported from viewRoster.py '''
''' Called on submit '''
def submitViewRoster(form_data):
    #print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #retrieves the data from the form for the sql query
    id = form_data.getfirst("TID") 
    return getRoster(str(id))

# Fetches the events of a given team
def getRoster(id):
    global curs
    
    #print "<p> right outside of checking for view: " #debugging
    #print view #debugging
    #user event query
    
    #print "<p>hello! Querying for user events for id No. " + id #debugging
    curs.execute('select name,PID from player inner join user where PID=UID and team=%s',(id,))
    

    # HTML Formatting below 
    header = "<div class=\"container\"><h2> Roster for team with ID:" + str(id) + "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> PID </th> \n <th> Player Name </th> \n </tr>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
        #print "<p>curs.fetchone: " #debugging
        #print row #debugging

        '''Advanced functionality of this would include using JSON to provide a sortable view of the events. We can implement this
        In the future.'''
        
        if row == None:
            # print "<h2> Events </h2>" + "\n".join(lines) #debugging 
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('PID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>" + "</tr>")
        # print lines #debugging
        
''' Imported from viewTeams.py '''
''' Called on submit '''
    #print "submit method in createTeam.py"
    #connect to the database
    global conn, curs
    conn = connect()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #retrieves the data from the form for the sql query
    id = form_data.getfirst("UID")  
    return getTeam(str(id))


# Fetches the events of a given team
def getTeam(id):
    global curs
    
    curs.execute('select name,TID from team inner join player where player.team=TID and PID=%s',(id,))
    
    # HTML Formatting below 
    header = "<div class=\"container\"><h2> Teams for user with ID:" + str(id) + "</h2> \n <hr>"
    tableHead = "<table class=\"table table-striped\"> <tr> \n <th> TID </th> \n <th> Team Name </th> \n </tr>"
    tableEnd = "</table></div>"

    lines = []    

    while True:
        row = curs.fetchone()
       	'''Advanced functionality of this would include using JSON to provide a sortable view of the events. We can implement this
        In the future.'''
        
        if row == None:
            return header + tableHead + "\n".join(lines) + tableEnd
        lines.append("<tr>" + "<td>" +  str(row.get('TID')) + "</td>")
        lines.append("<td>" + row.get('name') + "</td>" + "</tr>")



''' Useful functions'''

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
