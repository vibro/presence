#!/usr/local/bin/python2.7

import sys
import cgi
import viewEvents
import cgi_utils_sda
import cgitb; cgitb.enable()



'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template) 
    return str.format(response=string)

def main():
  # Conditionals that determine what action to take
  #cgi.test()
  global form_data
  form_data = cgi.FieldStorage()
  submit_type = form_data.getfirst("submit")
  return viewEvents.submit(form_data, submit_type) #returns an html representation of the events


if __name__ == "__main__":
    print "Content-type: text/html\n"

    print render_webpage('./presence/viewEvents.html',main()) 
