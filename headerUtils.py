import sys
import cgi
import cgi_utils_sda
import cgitb; cgitb.enable()
import session
import Cookie

def print_header(title):
    str = cgi_utils_sda.file_contents('header.html')
    return str.format(title=title)

def make_navbar():
    str = cgi_utils_sda.file_contents("navbar.html")
    #logged status printed so capital L on label, lower l on URL
    if logged_status():
        status = "ogout"
    else:
        status = "ogin"
    return str.format(status=status)

def logged_status():
    cookie = cgi_utils_sda.getCookieFromRequest("SESSID")
    if cookie == None:
        return False
    else: 
        return True
