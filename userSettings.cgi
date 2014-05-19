#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import userSettings
import headerUtils

def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar() 
    return str.format(navbar=navbar,string=string)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data = cgi.FieldStorage()
    print headerUtils.print_header("User Settings")
    print render_webpage('userSettings.html', userSettings.submit(form_data))
    
