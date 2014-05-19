#!/usr/local/bin/python2.7
import sys
import cgi
import createEvent
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils
import session


'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar()
    team = session.getTeamName()
    return str.format(navbar=navbar,string=string,team=team)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data = cgi.FieldStorage()
    print headerUtils.print_header("Create Event")
    print render_webpage('createEvent.html',createEvent.submit(form_data))
