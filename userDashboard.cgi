#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()


def makeButtons(UID):
    buttons='''
    <p><a class="btn btn-primary btn-lg" href="viewTeams.cgi?UID='''+UID+'''" role="button">My Teams</a>
    <p><a class="btn btn-primary btn-lg" href="viewEvents.cgi?view=user&ID='''+UID+'''" role="button">My Events</a>
    <p><a class="btn btn-primary btn-lg" href="index.html" role="button">Settings</a>
'''
    return buttons

def render_webpage(template,UID):
    str = cgi_utils_sda.file_contents(template)
    buttons = makeButtons(UID)
    return str.format(buttons=buttons)


if __name__ == "__main__":
    print "Content-type: text/html\n"   
    print render_webpage('userDash.html',"1")
    
