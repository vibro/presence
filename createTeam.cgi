#!/usr/local/bin/python2.7

import sys
import cgi
import createTeam
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils


'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template) 
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,string=string)


if __name__ == "__main__":
    headerUtils.redirect()
    main()
    form_data = cgi.FieldStorage()
    createTeam.submit(form_data) #creates a team
    print headerUtils.print_header("Create Team")
    print render_webpage('createTeam.html',"")
