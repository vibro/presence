#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import addMember
import headerUtils
import session

def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar() 
    team = session.getTeamName()
    return str.format(navbar=navbar,string=string,team=team)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data = cgi.FieldStorage()
    
    print headerUtils.print_header("Add Member")
    print render_webpage('addMember.html', addMember.submit(form_data))
    
