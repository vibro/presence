#!/usr/local/bin/python2.7

import sys
import cgi
import viewRoster #PROBABLY WILL CHANGE THIS
import cgi_utils_sda
import cgitb; cgitb.enable()
import headerUtils


'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template) 
    navbar = headerUtils.make_navbar()
    return str.format(navbar=navbar,string=string)

def main():
  # Conditionals that determine what action to take
  #cgi.test()
  global form_data
  form_data = cgi.FieldStorage()
  return viewRoster.submit(form_data) #returns an html representation of the events


if __name__ == "__main__":
    headerUtils.redirect()
    print headerUtils.print_header("View Roster")
    print render_webpage('viewRoster.html',main()) 
