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
    #TODO if team is deleted, fix header

    if type == "m" or type == "c" and (team != "None" or team != "NULL" or team != None):
        dashboard = "<li><a href='managerDashboard.cgi'>Manage Team: "+team+"</a></li>"
        switch = "<li><a href='viewTeams.cgi'>Switch Team </a></li>"
        
    elif type == "p" and (team != "None" or team != None):
        dashboard = "<li><a href='playerDashboard.cgi'>View Team: "+team+"</a></li>"
        switch = "<li><a href='viewTeams.cgi'>Switch Team </a></li>"
       
    else:
        dashboard = ""
        switch = ""
       

    #logged status printed so capital L on l abel, lower l on URL
    if logged_status():
        status = "ogout"
        userdash = "<li><a href='userDashboard.cgi'>My Dashboard</a></li>"
        settings ="<li><a href='userSettings.cgi'>Settings</a></li>"
        index = "#"
    else:
        status = "ogin"
        userdash = ""
        index = "index.cgi"
        settings = ""
    return str.format(index=index,userdash=userdash,dashboard=dashboard,status=status,team=team,switch=switch,settings=settings)

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

