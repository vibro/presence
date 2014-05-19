#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils
import session
import dashboard

def updateTables(TID):
    UID = session.getUserFromSession()
    session.setTeam(TID)
    if (dashboard.isManager(UID,TID)):
        session.setStatus('m')
        return "m"
    elif (dashboard.isCoach(UID,TID)):
        session.setStatus('c')
        return "c"
    elif (dashboard.isMember(UID,TID)):
        session.setStatus('p')
        return "p"
    else:
        session.setStatus("NULL")
        return None

if __name__ == "__main__":
    print "Content-type: text/html"
    form_data = cgi.FieldStorage()
    TID = form_data.getfirst('TID')
    status = updateTables(TID)
    if status == "m" or status == "c":
        print "Location:managerDashboard.cgi \n"
    elif status == "p":
        print "Location:playerDashboard.cgi \n"
    else:
        print "Location:viewTeams.cgi \n"
        




