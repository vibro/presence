#!/usr/local/bin/python2.7

# Credentials to access databases as the webdb user.

# Also creates a function to replace the MySQL.connect method and
# reassigns the error class, so that we reduce the number of dependencies
# on MySQLdb

import MySQLdb

Error = MySQLdb.Error

# this is essentially a static variable of this package

the_database_connection = False

def connect(dsn):
    '''Returns a database connection/handle given the dsn (a dictionary)

This function saves the database connection, so if you invoke this again,
it gives you the same one, rather than making a second connection.  This
is the so-called Singleton pattern.'''
    global the_database_connection
    if not the_database_connection:
        try:
            the_database_connection = MySQLdb.connect( host=dsn['hostname'],
                                                       user=dsn['username'],
                                                       passwd=dsn['password'],
                                                       db=dsn['database'])
            # so each modification takes effect automatically
            the_database_connection.autocommit(True)
        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
    return the_database_connection

if __name__ == '__main__':
    print 'starting test code'
    import sys
    if len(sys.argv) < 2:
        print '''Usage: {cmd} DSNfile
test dbconn by giving the name of a DSN file on the command line'''.format(cmd=sys.argv[0])
        sys.exit(1)
    dsnfile = sys.argv[1]
    module = __import__(dsnfile)
    DSN = module.DSN
    DSN['database']='wmdb'
    c = connect(DSN)
    print 'successfully connected'
    curs = c.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select user() as user, database() as db')
    row = curs.fetchone()
    print 'connected to {db} as {user}'.format(db=row['db'],user=row['user'])
    
