#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils
import session


def render_webpage(template):
    str = cgi_utils_sda.file_contents(template)
    
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar)

if __name__ == "__main__":
    #headerUtils.redirect()
    print cgi_utils_sda.cgi_header()
    print headerUtils.print_header("Welcome")
    print render_webpage('index.html')
    
