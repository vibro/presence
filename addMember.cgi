#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import addMember


def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    return str.format(string=string)


if __name__ == "__main__":
    print "Content-type: text/html\n"
    form_data = cgi.FieldStorage()
    addMember.submit(form_data) #creates an event for a team
    
    print render_webpage('presence/addMember.html',"")
    