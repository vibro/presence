#!/usr/local/bin/python2.7

import sys
import cgi
import createTeam
import cgi_utils_sda
import cgitb; cgitb.enable()


def main():
  # Conditionals that determine what action to take
  #cgi.test()
  global form_data
  form_data = cgi.FieldStorage()
  createTeam.submit(form_data) #creates a team


if __name__ == "__main__":
    print "Content-type: text/html\n"
    main()
#    tmpl = cgi_utils_sda.file_contents("~hye/public_html/presence/createTeam.html")
#    print(tmpl)