#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils
import session
import dashboard

def makeButtons(TID,UID):
    buttons='''
    <p><a class="btn btn-primary btn-lg" href="viewRoster.cgi?TID='''+TID+'''" role="button">Roster</a>
    <p><a class="btn btn-primary btn-lg" href="viewEvents.cgi?view=user&ID='''+UID+'''" role="button">My Team's Events</a>
    <p><a class="btn btn-primary btn-lg" href="index.html" role="button">Update Player Profile</a>
'''
    #TODO: CHANGE LAST BUTTON
    return buttons

def render_webpage(template,TID,UID):
    str = cgi_utils_sda.file_contents(template)
    buttons = makeButtons(TID,UID)
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,buttons=buttons)


if __name__ == "__main__":
    headerUtils.redirect()
    TID = session.getTeamFromSession()
    UID = session.getUserFromSession()
    print headerUtils.print_header("Player Dashboard")
    print render_webpage('playerDash.html',TID,UID)
    
