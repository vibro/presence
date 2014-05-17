#!/usr/local/bin/python2.7

import os
import sys
import cgi
import Cookie
import cgi_utils_sda
import cgitb; cgitb.enable()
import session
import headerUtils


def logout(sessid):
    if session.existsSession(sessid):
        session.deleteSession(sessid)
        cookie = setCookie(None,-1)
        return cookie

def setCookie(sessid,expires=None):
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie,'SESSID',sessid,expires)
    return sesscookie

def main():
    cookie = cgi_utils_sda.getCookieFromRequest("SESSID")
    cookieval = cookie.value
    cookie2 = logout(cookieval)
    cgi_utils_sda.print_headers(cookie2,"Location:login.cgi")

    
if __name__ == '__main__':
    main()
                
