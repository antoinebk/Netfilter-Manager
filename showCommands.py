#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="antoine"
__date__ ="$10 aout 2010 16:04:18$"

# IMPORTS
import configuration
import sqlite3 as sqlite

# FUNCTIONS

def showHosts():

    # Intro
    print ""
    print "   Hosts known by netfilter Manager"
    print "   --------------------------------"
    
    # Connecting to SQLite DB
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()
    
    # Getting all the hostname and IPs
    cursor.execute("SELECT name, ip FROM host;")
    
    for row in cursor:
        print "    - "+row[0]+" @ "+row[1]

    print ""
    cursor.close()

def showVersion():
    print "Version : 0.1"

def showAccessList(host,raw):

    # Connecting to SQLite DB
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()

    if raw == 0:

        # Get the rules for the host
        cursor.execute("SELECT rules.line, rules.rule FROM rules, host WHERE host.name=? AND host.id=rules.host_id ORDER BY line",[host])
        
        print ""
        print "Iptables rules for host "+host
        print ""
        
        for row in cursor:
            print str(row[0])+': '+str(row[1])

        print ""
        print "Note : first number is the line number for the rule"
        
        # Close down
        cursor.close()

    elif raw == 1:

        # Get the rules for the host
        cursor.execute("SELECT rules.rule FROM rules, host WHERE host.name=? AND host.id=rules.host_id ORDER BY line",[host])

        # Initialize variable
        rules = ''

        for row in cursor:
            rules += str(row[0])+'\n'

        print rules
        cursor.close()
