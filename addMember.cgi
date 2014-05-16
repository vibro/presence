#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import addMember
import headerUtils

def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar() 
    return str.format(navbar=navbar,string=string)


if __name__ == "__main__":
    print "Content-type: text/html\n"
    form_data = cgi.FieldStorage()
    addMember.submit(form_data) #creates an event for a team

    print headerUtils.print_header("Add Member")
    print render_webpage('addMember.html',"")
    
