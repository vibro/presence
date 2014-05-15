#!/usr/local/bin/python2.7

import os
import sys
import cgi
import Cookie
import datetime
import cgi_utils_sda
import cgitb; cgitb.enable()
import session

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

def session_start(dir):
    '''Intended to mimic the behavior of the PHP function of this name,
except that instead of creating a "superglobal," this will just return
a data structure that can be used in set_session_value and get_session_value.
It takes as an argument the directory to read session data from.'''
    sessid = session_id()
# Set a cookie and print that header
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie(SESS_ID,sessid))
    print(sesscookie)
    # check to see if there's any session data
    # session already exists, so load saved data
    # rb for read binary
    input = open(dir+sessid,'r')
    sess_data = pickle.load(input)
    input.close()
    if isinstance(sess_data,dict):
        return sess_data
    else:
        raise Exception ("Possibly corrupted session data; not a dictionary: "
                         +sess_data)
        return

def save_session(form_data):
    global SESS_ID
    '''Save the session data to the filesystem.'''
    sessid = session_id()
    
    session.submitLogin(form_data,sessid)

def set_cookie(sessid):
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie,SESS_ID,sessid)
    return sesscookie

def logout(sessid):
    if session.existsSession(sessid):
        session.deleteSession(sessid)
        cookie = set_cookie('')
        return cookie
def main():
    #print "Content-type: text/html\n"
    form_data = cgi.FieldStorage()
    if (form_data.getfirst('login') is not None):
        cookie = set_cookie(session_id())
        cgi_utils_sda.print_headers(cookie)
        save_session(form_data)
    elif (form_data.getfirst('logout') is not None):
        cookie = logout(session_id())
        cgi_utils_sda.print_headers(cookie)
        print cookie
        
    else:
        cgi_utils_sda.print_headers(None)
    print_page("","Cool i guess")


def print_page(cookie,message):
    template = cgi_utils_sda.file_contents('login.html')
    print template.format(cookie=cookie,text=message,msg="")


 
if __name__ == '__main__':
    main()
