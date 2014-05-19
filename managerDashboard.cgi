#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils

def makeButtons(TID):
    buttons='''
    <p><a class="btn btn-primary btn-lg" href="viewRoster.cgi?TID='''+TID+'''" role="button">Roster</a>
    <p><a class="btn btn-primary btn-lg" href="viewEvents.cgi?view=team&ID='''+TID+'''" role="button">My Events</a>
    <p><a class="btn btn-primary btn-lg" href="addMember.cgi" role="button">Add Members</a>
    <p><a class="btn btn-primary btn-lg" href="createEvent.cgi" role="button">Create Event</a>
'''
    return buttons

def render_webpage(template,TID):
    str = cgi_utils_sda.file_contents(template)
    buttons = makeButtons(TID)
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,buttons=buttons)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data=cgi.FieldStorage()
    TID = form_data.getfirst("TID")
    print headerUtils.print_header("Manager Dashboard")
    print render_webpage('managerDash.html',TID)
    
