#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils
import session

def makeButtons(UID):
    buttons='''
    <p><a class="btn btn-primary btn-lg" href="viewTeams.cgi" role="button">My Teams</a>
    <p><a class="btn btn-primary btn-lg" href="viewEvents.cgi?view=user" role="button">My Events</a>
    <p><a class="btn btn-primary btn-lg" href="createTeam.cgi" role="button">Create Team</a>
    <p><a class="btn btn-primary btn-lg" href="userSettings.cgi" role="button">Settings</a>
'''
    return buttons

def render_webpage(template,UID):
    str = cgi_utils_sda.file_contents(template)
    buttons = makeButtons(UID)
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,buttons=buttons)

if __name__ == "__main__":
    headerUtils.redirect()
    print headerUtils.print_header("User Dasboard")
    UID = session.getUserFromSession()
    print render_webpage('userDash.html',UID)
    
