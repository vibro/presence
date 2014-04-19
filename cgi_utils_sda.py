#!/usr/local/bin/python2.7

import sys
import os
import Cookie
import datetime

# Copied code from Lyn Turbak's utilities

def file_contents(filename):
    '''Returns contents of file as a string.'''
    file = open(filename,"r")
    contents = file.read()
    file.close()
    return contents

def arglist_to_hash(list):
    '''Returns a hash, like cgi.FieldStorage of the list.

    Useful for using or testing a CGI script from the command line.
    Modeled after the perl CGI module's testing feature.  Typically, the
    argument is sys.argv, but could be any list of the form key=value'''
    hash = {}
    for arg in list:
        key,value = arg.split('=')
        hash[key] = value
    return hash

def cgi_header():
    '''Prints the text/html header for simple web content

See print_headers() if you want to handle cookies'''
    return "Content-type: text/html\n\n"

def check_required_inputs(hash,keys):
    '''Checks whether the hash has all the keys in the list; returns a
    list of error message about missing keys.'''
    errors = []
    for key in keys:
        if not hash.has_key(key):
            errors.append('Required key %s is missing' % (key,))
    return errors

# ================================================================
# Cookie stuff

def setCookie(response_cookie,name,value,expires=None,path='/'):
    '''Takes a Cookie object (set of morsels) and sets one morsel.

If no expiration is set, default is 5 minutes from now.  Returns the modified Cookie object'''
    response_cookie[name] = value
    response_cookie[name]["path"] = path
    if expires == None:
        # default is to expire 5 minutes from now
        expires = datetime.datetime.now()+datetime.timedelta(minutes=5)
    response_cookie[name]["expires"] = expires
    return response_cookie

def getCookieFromRequest(cookiename):
    '''This returns the named cookie (as an object), or None if it does not exist'''
    try:
        cookies = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        return cookies[cookiename]
    except (Cookie.CookieError, KeyError):
        return None

def print_headers(cookie):
    '''Prints the headers of the response, including the cookie, if any.

You can supply None as the cookie if you do not want any cookies set in the response.'''
    # actually, it would work just to print the (empty) cookie, as the
    # output() method produces an empty string.  But this way, you can
    # change your mind about setting cookies, even after setting some.
    print 'Content-type: text/html'
    if cookie != None: 
        print cookie.output()
    print '\n'

# ================================================================

def unique_id():
    '''Returns the Apache-generated UNIQUE_ID, suitable for session keys and such'''
    try: 
        return os.environ['UNIQUE_ID']
    except KeyError:
        sys.exit("Could not determine UNIQUE_ID")
    
def showhash(hash):
    '''Returns an HTML unordered list displaying the keys and values'''
    keys = hash.keys()
    keys.sort()
    result = '<ul>\n'
    for key in keys:
        result += '<li>'+key+' &rarr; '+hash[key]+'\n'
    result += '</ul>\n'
    return result
