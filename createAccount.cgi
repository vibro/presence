#!/usr/local/bin/python2.7

import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import createAccount
import headerUtils

def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template)
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,string=string)


if __name__ == "__main__":
    #headerUtils.redirect()
    print cgi_utils_sda.cgi_header()
    form_data = cgi.FieldStorage()


    print headerUtils.print_header("Create a New Account")
    print render_webpage('createAccount.html',createAccount.submit(form_data))
    
