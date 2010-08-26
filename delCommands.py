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

import checkCommands
import os
import configuration
import sqlite3 as sqlite
from shutil import move

def delHost(host):

    # Check if host exists
    if checkCommands.checkIfHostsExists(host) != 0:

        # Initialize answer variable
        answer = 'd'
        # Prompt if sure of deletion
        while answer != 'Y' and answer != 'n':
            answer = raw_input('Do you really want to delete host '+host+' and all the rules associated ? [Y/n] ')

        if answer == 'n':
            print 'Host deletion cancelled'
            return
        elif answer == 'Y':
            # Deleting host

            # Connecting to SQLite DB
            connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
            cursor = connection.cursor()

            # First delete all the rules tied to the host
            cursor.execute("DELETE FROM rules WHERE host_id=(SELECT id FROM host WHERE name=?);",[host])

            # Then delete the host
            cursor.execute("DELETE FROM host WHERE name=?",[host])

            # Commit and exit
            connection.commit()
            cursor.close()

            print 'Host successfully deleted'

    else:
        print 'Host deletion failed : Unknown host'

def delLine(host, linenumber):
    # Check if line number is correct
    try:
        int(linenumber)
    except:
        print 'Usage : line <#>. Deletes all rules on line in question.'
        return
    if int(linenumber) <= 0 or int(linenumber) > 200:
        print 'Line number must be less then or equal to 200 and greater then 0'
        return
    # Check if host exists
    if checkCommands.checkIfHostsExists(host) != 0:

        # Initialize answer variable
        answer = '?'
        # Prompt if sure of deletion
        while answer != 'Y' and answer != 'n':
            answer = raw_input('Do you really want to delete all the rules on line '+linenumber+' ? [Y/n] ')

        if answer == 'n':
            print 'Line deletion cancelled'
            return
        elif answer == 'Y':
            # Deleting all rules on line
            
            # Connecting to SQLite DB
            connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM rules WHERE host_id=(SELECT id from host WHERE name=?) AND line=?;",[host,linenumber])
            
            # Commit and exit
            connection.commit()
            cursor.close()

            print 'Line successfully deleted'

def delRule(host,rule):

    # Check if host exists
    if checkCommands.checkIfHostsExists(host) != 1:
        print 'Unknow host '+host
        return

    # Prompt if sure of deletion
    answer = '?'
    while answer != 'Y' and answer != 'n':
        answer = raw_input('Are you sure you want to delete this rule on all lines ? [Y/n] ')

    if answer == 'n':
        return

    # Connecting to SQLite DB
    connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM rules WHERE rule=? AND host_id=(SELECT id FROM host WHERE name=?)",[rule,host])

    # Commit and exit
    connection.commit()
    cursor.close()
