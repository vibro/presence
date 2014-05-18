#!/usr/local/bin/python2.7
import sys
import cgi
import createEvent
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils


'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,response=string)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data = cgi.FieldStorage()
    return createEvent.submit(form_data) #creates an event for a team
    print headerUtils.print_header("Create Event")
    print render_webpage('createEvent.html',main())
