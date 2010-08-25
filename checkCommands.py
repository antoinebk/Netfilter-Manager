#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

import configuration
import socket
import sys
import sqlite3 as sqlite

def checkIfHostsExists(hostname):

    # Initialize found variable
    found = 0

    # Connecting to SQLite DB
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()

    # Read the hosts from DB
    cursor.execute("SELECT name FROM host;")

    for row in cursor:
        if row[0] == hostname:
            found = 1

    # Close cursor to DB
    cursor.close()

    # Return values of found : 1 if found, 0 if not found
    return found

def getHostIp(hostname):

    # First check if it exists :-)
    if checkIfHostsExists(hostname) == 1:

        # Connecting to SQLite DB
        connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
        cursor = connection.cursor()

        # Find IP related to host
        cursor.execute("SELECT ip FROM host WHERE name=?",[hostname])

        return str(cursor.fetchone()[0])

    else:
        print 'Cannot get IP or hostname of host : Host not found'
        return -1

def checkValidIp(ip):
    try:
        socket.inet_aton(ip)
        return 0
    except:
        return -1

def convertNetmasktoCIDR(netmask):

    # Couldn't find a prettier way to do this...

    # Default CIDR to bogus value
    cidr = -1

    if netmask == '255.255.255.255':
        cidr = 32
    elif netmask == '255.255.255.254':
        cidr = 31
    elif netmask == '255.255.255.252':
        cidr = 30
    elif netmask == '255.255.255.248':
        cidr = 29
    elif netmask == '255.255.255.240':
        cidr = 28
    elif netmask == '255.255.255.224':
        cidr = 27
    elif netmask == '255.255.255.192':
        cidr = 26
    elif netmask == '255.255.255.128':
        cidr = 25
    elif netmask == '255.255.255.0':
        cidr = 24
    elif netmask == '255.255.254.0':
        cidr = 23
    elif netmask == '255.255.252.0':
        cidr = 22
    elif netmask == '255.255.248.0':
        cidr = 21
    elif netmask == '255.255.240.0':
        cidr = 20
    elif netmask == '255.255.224.0':
        cidr = 19
    elif netmask == '255.255.192.0':
        cidr = 18
    elif netmask == '255.255.128.0':
        cidr = 17
    elif netmask == '255.255.0.0':
        cidr = 16
    elif netmask == '255.254.0.0':
        cidr = 15
    elif netmask == '255.252.0.0':
        cidr = 14
    elif netmask == '255.248.0.0':
        cidr = 13
    elif netmask == '255.240.0.0':
        cidr = 12
    elif netmask == '255.224.0.0':
        cidr = 11
    elif netmask == '255.192.0.0':
        cidr = 10
    elif netmask == '255.128.0.0':
        cidr = 9
    elif netmask == '255.0.0.0':
        cidr = 8
    elif netmask == '254.0.0.0':
        cidr = 7
    elif netmask == '252.0.0.0':
        cidr = 6
    elif netmask == '248.0.0.0':
        cidr = 5
    elif netmask == '240.0.0.0':
        cidr = 4
    elif netmask == '224.0.0.0':
        cidr = 3
    elif netmask == '192.0.0.0':
        cidr = 2
    elif netmask == '128.0.0.0':
        cidr = 1
    elif netmask == '0.0.0.0':
        cidr = 0

    # Return CIDR but it it's value is -1 we will know the netmask is invalid
    return cidr

def checkConfiguration():

    # Check if config file was edited
    if configuration.basedir == '' or configuration.datadir == '' or configuration.starttpl == '':
        print 'ERROR : You must first edit the configuration file "configuration.py"'
        print 'Exiting...'
        sys.exit(0)

    # Check if sqlite database has the required tables
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()

    # Check if there are any tables
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()

    # Check if result is empty
    if len(result) == 0:
        # Tell the user that we have not found any tables
        print 'No SQLite tables found...'

        # Create the appropriate tables then :-)
        print 'Creating SQLite tables...'
        # Creating hosts table
        cursor.execute("CREATE TABLE host (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100), ip VARCHAR(100), type VARCHAR(20));")
        # Creating rules table
        cursor.execute("CREATE TABLE rules (id INTEGER PRIMARY KEY AUTOINCREMENT, line INTEGER, host_id INTEGER, rule VARCHAR(500));")
        # Commiting and closing down
        connection.commit()
        cursor.close()

    elif len(result) == 2:
        hosttablefound=False
        rulestablefound=False

        # Check tables created
        for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall():
            if str(table).split("'")[1] == 'host':
                hosttablefound=True
            elif str(table).split("'")[1] == 'rules':
                rulestablefound=True

        # Fail if both tables not found (must be trying to use some other DB...)
        if not hosttablefound or not rulestablefound:
            print 'ERROR : Found a SQLite DB but not containing the tables we wanted.'
            sys.exit(0)
    
    elif len(result) > 3:
        print 'ERROR : Found a SQLite DB but containing more tables then we expected.'
        print 'Found tables : ',
        for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall():
            print table,
        print ''
        sys.exit(0)