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
    type = session.getStatus()
    team = session.getTeamName()
    if type == "m" or type == "c":
        dashboard = "<li><a href='managerDashboard.cgi'>Manage Team: "+team+"</a></li>"
    elif type == "p":
        dashboard = "<li><a href='playerDashboard.cgi'>View Team: "+team+"</a></li>"
    else:
        dashboard = ""
    
    
        

    #logged status printed so capital L on l abel, lower l on URL
    if logged_status():
        status = "ogout"
    else:
        status = "ogin"
    return str.format(dashboard=dashboard,status=status,team=team)

def logged_status():
    cookie = cgi_utils_sda.getCookieFromRequest("SESSID")
    if cookie == None:
        return False
    else: 
        return True

def redirect(cookie=None,location="Location:login.cgi"):
    if logged_status():
        cgi_utils_sda.print_headers(cookie)
    else:
        cgi_utils_sda.print_headers(cookie,location)

