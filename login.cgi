#!/usr/local/bin/python2.7

import os
import sys
import cgi
import pickle
import Cookie
import datetime
import cgi_utils_sda
import cgitb; cgitb.enable()

PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie
 
def session_id():
    '''Intended to mimic the behavior of the PHP function of this name'''
    sesscookie = cgi_utils_sda.getCookieFromRequest(PY_CGI_SESS_ID)
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
    cgi_utils_sda.setCookie(sesscookie,PY_CGI_SESS_ID,sessid)
    print(sesscookie)
    # check to see if there's any session data
    if not os.path.isfile(dir+sessid):
        return {}
    output = open(dir+sessid,'r+')
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

def save_session(dir,data):
    '''Save the session data to the filesystem.'''
    sessid = session_id()
    output = open(dir+sessid,'w+')
    pickle.dump(data,output,-1)
    output.close()
 
def main():
    print "Content-type: text/html\n"
    my_sess_dir = '/sessions/'
    sess_data = session_start(my_sess_dir)
    print_page("","I'm not sure what's happening")


def print_page(cookie,message):
    template = cgi_utils_sda.file_contents('login.html')
    print template.format(cookie=cookie,text=message,msg="")


 
if __name__ == '__main__':
    main()
