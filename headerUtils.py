import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()

def print_header(title):
    str = cgi_utils_sda.file_contents('header.html')
    return str.format(title=title)

def make_navbar():
    str = cgi_utils_sda.file_contents("navbar.html")
    return str.format()
