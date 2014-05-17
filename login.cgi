#!/usr/local/bin/python2.7

import os
import sys
import cgi
import Cookie
import datetime
import cgi_utils_sda
import cgitb; cgitb.enable()
import session
import headerUtils

SESS_ID='SESSID'   # a constant, the name of the cookie
 
def session_id():
    '''Intended to mimic the behavior of the PHP function of this name'''
    sesscookie = cgi_utils_sda.getCookieFromRequest(SESS_ID)
    if sesscookie == None:
        sessid = cgi_utils_sda.unique_id()
        if sessid == None:
            print("I give up; couldn't create a session. No session id")
            return
    else:
        sessid=sesscookie.value   # get value out of morsel
    return sessid

def save_session(form_data):
    global SESS_ID
    '''Save the session data to the database.'''
    sessid = session_id()
    
    return session.submitLogin(form_data,sessid)

def set_cookie(sessid,expires=None):
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie,SESS_ID,sessid,expires)
    return sesscookie

def logout(sessid):
    if session.existsSession(sessid):
        session.deleteSession(sessid)
        cookie = set_cookie(None,-1)
        return cookie

def main():
    form_data = cgi.FieldStorage()
    error = ""
    if (form_data.getfirst('login') is not None):
        exists,UID = save_session(form_data)
        if exists is False: 
            error = "Invalid email or password"
            cgi_utils_sda.print_headers(None)
        else:
            cookie = set_cookie(session_id())
            cgi_utils_sda.print_headers(cookie,"Location:userDashboard.cgi")
            session.setUserSession(session_id(),UID)
            error = "Login successful"
    elif (form_data.getfirst('logout') is not None):
        cookie = logout(session_id())
        cgi_utils_sda.print_headers(cookie)

    else:
        cgi_utils_sda.print_headers(None)

    print headerUtils.print_header("Log in")
    print_page(error)


def print_page(message):
    template = cgi_utils_sda.file_contents('login.html')
    navbar = headerUtils.make_navbar()
    print template.format(navbar=navbar,message=message)

 
if __name__ == '__main__':
    main()
    

    
