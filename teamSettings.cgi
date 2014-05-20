#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import teamSettings
import headerUtils

def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar() 
    return str.format(navbar=navbar,string=string)


if __name__ == "__main__":
    headerUtils.redirect()
    form_data = cgi.FieldStorage()
    print headerUtils.print_header("Team Settings")
    if form_data.getfirst('delete') != None:
        print render_webpage('teamSettings.html', teamSettings.delete())
    elif form_data.getfirst('submit') != None:
        print render_webpage('teamSettings.html', teamSettings.submit(form_data))
    else:
        print render_webpage('teamSettings.html', "")
