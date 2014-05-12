#!/usr/local/bin/python2.7
import sys
import cgi
import createEvent
import cgi_utils_sda
import cgitb; cgitb.enable()
import functions



'''Method that prints out the appropriate webpage'''
def render_webpage(template,string):
    str = cgi_utils_sda.file_contents(template) 
    return str.format(string=string)

def main():
  # Conditionals that determine what action to take
  #cgi.test()
  global form_data
  form_data = cgi.FieldStorage()
  functions.submitCreateEvent(form_data) #creates an event for a team


if __name__ == "__main__":
    print "Content-type: text/html\n"
    main()
    print render_webpage('createEvent.html',"")
