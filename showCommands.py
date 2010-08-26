# netfilterManager
#Copyright (C) 2010  Antoine Benkemoun
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
