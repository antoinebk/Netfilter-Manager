#! /usr/bin/python

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

# To change this template, choose Tools | Templates
# and open the template in the editor.

# IMPORTS
import configuration
import socket
import checkCommands
import writeCommands
import sqlite3 as sqlite

def addHost(hostname,ip):

    # Check for forbidden hostname 'none'
    if hostname == 'none':
        print 'Forbidden name for host : none'
        return
    elif hostname == 'all':
        print 'Forbidden name for host : all'
        return

    # use check function
    found = checkCommands.checkIfHostsExists(hostname)
    
    if found == 0:

        # Add host to DB
        # Connecting to SQLite DB
        connection = sqlite.connect(configuration.basedir+configuration.datadir+"/db")
        cursor = connection.cursor()

        # Creating host
        data=[str(hostname),str(ip)]
        cursor.execute("INSERT INTO host (name, ip, type) VALUES(?,?,'Linux');",data)

        # Commit
        connection.commit()

        # Close the cusor
        cursor.close()

        print "Host successfully added."

    else:
        print 'Add host failed : Duplicate host.'
        return

def addTemplateToHost(host,linenumber,command):
    # Check if length is correct and display help
    if len(command.split()) == 1:
        print 'Too few arguments. Type template help for help.'
        return
    if len(command.split()) == 2 and command.split()[1] == 'help':
        print 'Usage : template <template-name> <arg1> <arg2> ...'
        print 'Note : The arguments are mentionned in your template and need to give here.'
        return
    # Check if host exists first
    if checkCommands.checkIfHostsExists == 0:
        print 'Unknow host '+hostname+'. Type help for help.'
        return

    # Give variables a friendlier name
    templatename = command.split()[1]

    # Check if template exists
    try:
        tplfile = open(configuration.basedir+configuration.tpldir+'/'+templatename+'.tpl', 'r')
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        print 'Template not found.'
        return

    # Initialize variables
    start = 0
    arguments = ''

    for line in tplfile:
        # Check if this is arguments line
        if line.startswith('arguments =') or line.startswith('arguments='):

            # Get all the arguments on the line in question
            for argument in str(line.split('=')[1]).strip().split(','):
                arguments += argument

        # Write the rules to the appropriate file. Default to line 200
        if start == 1 and line != '\n':
            # Replace the variables
            # Initialize an index that will go through all the arguments give in the command
            index = 2
            for argument in arguments.split():
                line = line.replace('{'+str(argument)+'}',str(command.split()[index]))
                index +=1
            # Write rule to file
            writeCommands.writeIptablesRule(host,linenumber,line.strip('\n'))
            
        # Check if template started
        if line.startswith('TEMPLATE-START'):
            # Check if we were given the right number of arguments
            if int(len(arguments.split())) != int(len(command.split()) - 2):
                print 'Number of arguments given incorrect. This template requires '+str(len(arguments.split()))+' arguments and you gave '+str(len(command.split()) - 2)+' arguments.'
                return
            start = 1



def addAccessListUsage(type):

    # Print different usage for different access lists
    if type == 'ip':
        print ''
        print 'Usage : '
        print ' - access-list {input|output} {allow|deny} ip <SOURCE> <DESTINATION>'
        print ''
        print '<SOURCE> and <DESTINATION> can be :'
        print ' - host <x.x.x.x>'
        print ' - any'
        print ' - <subnet> <subnet-mask>'
        print ''
        print 'Note : '
        print ' - You can replace an IP or subnet by the keyword any if you do not wish to specify one.'
        print ''
        return

    if type == 'tcp' or type == 'udp':
        print ''
        print 'Possible usages :'
        print ' - access-list {input|output} {allow|deny} {tcp|udp} host <x.x.x.x> host <y.y.y.y> eq portnumber'
        print ' - access-list {input|output} {allow|deny} {tcp|udp} <x.x.x.x> portnumber <y.y.y.y> portnumber'
        print ''
        print 'Note : You can replace an IP or a port number by the keyword any if you do not wish to specify one.'
        print ''

    else:
        print ''
        print 'Possible usages :'
        print ' - access-list {input|output} {allow|deny} {tcp|udp} host <x.x.x.x> host <y.y.y.y> eq zz'
        print ' - access-list {input|output} {allow|deny} {tcp|udp} <x.x.x.x> {portnumber|any} <y.y.y.y> {portnumber|any}'
        print ' - access-list {input|output} {allow|deny} ip host <x.x.x.x> host <y.y.y.y>'
        print ''
        print 'Note : You can replace an IP or a port number by the keyword any if you do not wish to specify one.'
        print ''

def generateIPRule(direction, policy, ipsource,ipdestination):

    # Translate policy from Cisco-speak to iptables-speak
    if policy == 'allow':
        policy = 'ACCEPT'
    elif policy == 'deny':
        policy = 'DROP'

    return 'iptables -A '+direction.upper()+' -s '+ipsource+' -d '+ipdestination+' -j '+policy

def addAccessList(command):

    # check if number of arguments is just 1 or lower
    if len(command.split()) < 2:
        print 'Access-list rule add failed : Too few arguments. Use "access-list help" for help'
        return

    # Check if number of argument is too low
    elif len(command.split()) < 6 and command.split()[1] != 'help':
        print 'Access-list rule add failed : Too few arguments. Use "access-list help" for help'
        return

    # Check for help
    elif len(command.split()) == 2 and command.split()[1] == 'help':
        addAccessListUsage('other')
        return

    # Support access-list help command
    elif len(command.split()) == 3 and command.split()[1] == 'help':

        helptype = command.split()[2]

        if helptype == 'ip':
            addAccessListUsage('ip')
            return
        elif helptype == 'tcp' or helptype == 'udp':
            addAccessListUsage('tcp')
            return
        else:
            addAccessListUsage('other')
            return

    # Check if direction is correct
    direction = command.split()[1]

    if direction != 'input' and direction != 'output':
        print 'Access-list rule add failed : Invalid flow direction. Use "access-list help" for help.'
        return

    # Check if policy is correct
    policy = command.split()[2]

    if policy != 'allow' and policy != 'deny':
        print 'Access-list rule add failed : Invalid policy keyword. Use "access-list help" for help.'
        return

    # Parse protocol
    protocol = command.split()[3]

    # check if protocol is correct
    if protocol != 'tcp' and protocol != 'udp' and protocol != 'ip':
        print 'Access-list rule add Failed : Invalid protocol '+protocol+'. Use "access-list help" for help'
        return

    #
    # IP PROTOCOL ACCESS-LIST CREATION
    #
    
    if protocol == 'ip':

        # Check if first keyword is any and length is correct
        if command.split()[4] == 'any' and len(command.split()) >= 6 and len(command.split()) <= 7:
            ipsource = '0/0'

            # Check if next keyword is any and length is correct
            if command.split()[5] == 'any' and len(command.split()) == 6:
                ipdestination = '0/0'

            # Check if next keyword is host and length is correct
            elif command.split()[5] == 'host' and len(command.split()) == 7:

                # Check if it's a correct destination IP
                try:
                    socket.inet_aton(command.split()[6])
                    ipdestination = command.split()[6]
                except:
                    print 'Access-list rule add failed : Invalid destination IP'
                    return
            
            # Check is next keyword is IP address and next+1 is netmask
            elif checkCommands.checkValidIp(command.split()[5]) != -1 and checkCommands.convertNetmasktoCIDR(command.split()[6]) != -1:
                # Convert mask to CIDR
                cidrmask = str(checkCommands.convertNetmasktoCIDR(command.split()[6]))
                # Compile destination IP : IP + / + cidr mask
                ipdestination = command.split()[5]+'/'+cidrmask

            else:
                print 'Access-list rule add failed : Invalid second keyword. Use "access-list help ip" for help.'
                return
                
        # Check if first keyword is host and length is correct
        elif command.split()[4] == 'host' and len(command.split()) <= 8 and len(command.split()) >= 7:

            # Check if following is any or a source IP
            if command.split()[5] == 'any':
                ipsource = '0/0'

            else:
                # Check if it's a correct source IP
                try:
                    socket.inet_aton(command.split()[5])
                    ipsource = command.split()[5]
                except:
                    print 'Access-list rule add failed : Invalid source IP. Use "access-list help ip" for help.'
                    return

            # Check if second keyword is host
            if command.split()[6] == 'host' and len(command.split()) == 8:

                # Check if following is any or destination IP
                if command.split()[7] == 'any' and len(command.split()) == 7:
                    ipdestination = '0/0'
                else:
                    # Check if it's a correct destination IP
                    try:
                        socket.inet_aton(command.split()[7])
                        ipdestination = command.split()[7]
                    except:
                        print 'Access-list rule add failed : Invalid destination IP. Use "access-list help ip" for help.'
                        return

            # Check if second keyword is any
            elif command.split()[6] == 'any' and len(command.split()) == 7:
                ipdestination = '0/0'

            # Check if second keyword is IP address and next+1 is netmask
            elif checkCommands.checkValidIp(command.split()[6]) != -1 and checkCommands.convertNetmasktoCIDR(command.split()[7]) != -1:
                # Convert mask to CIDR
                cidrmask = str(checkCommands.convertNetmasktoCIDR(command.split()[7]))
                # Compile destination IP : IP + / + cidr mask
                ipdestination = command.split()[6]+'/'+cidrmask

            else:
                print 'Access-list rule add failed : Invalid second keyword. Use "access-list help ip" for help.'
                return

        # Check if first keyword is IP and Netmask
        elif checkCommands.checkValidIp(command.split()[4]) != -1 and checkCommands.convertNetmasktoCIDR(command.split()[5]) != -1:

            # Convert netmask to CIDR
            cidrmask = checkCommands.convertNetmasktoCIDR(command.split()[5])
            # Compose the source IP : ip + / + CIDRMask
            ipsource = command.split()[4]+'/'+str(cidrmask)

            # Check if next keyword is any
            if command.split()[6] == 'any':
                ipdestination = '0/0'

            # Check if next keyword is host
            elif command.split()[6] == 'host':
                # check if destination IP is valid
                if checkCommands.checkValidIp(command.split()[7]) != -1:
                    ipdestination = command.split()[7]
                else:
                    print 'Access-list rule add failed : Invalid IP. Use "access-list help ip" for help.'

            # Check if next keyword is IP address and next+1 is netmask
            elif checkCommands.checkValidIp(command.split()[6]) != -1 and checkCommands.convertNetmasktoCIDR(command.split()[7]) != -1:
                # Convert netmask to CIDR
                cidrmask = checkCommands.convertNetmasktoCIDR(command.split()[7])
                # Compose the destination IP : ip + / + CIDRMask
                ipdestination = command.split()[6]+'/'+str(cidrmask)

            else:
                print 'Access-list rule add failed : Invalid second keyword. Use "access-list help ip" for help.'
                return

        else:
            # Check if first keyword is IP address and next keyword is netmask
            print 'Access-list rule add failed : Invalid first keyword. Use "access-list help ip" for help.'
            return

        # After all this, we should be fine (or at least we hope so)
        rule = generateIPRule(direction,policy,ipsource,ipdestination)
        return rule