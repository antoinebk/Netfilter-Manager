#! /usr/bin/python

import checkCommands
import configuration
import showCommands
import subprocess
import os

def pushSSH(command):

    # Check if length of command is correct
    if len(command.split()) == 2:
        
        # Give variables a friendlier name
        host = command.split()[1]

        # Check if host exists
        if checkCommands.checkIfHostsExists(host):
            
            # Ask for user
            user = raw_input('Username: ')

            # Ask for remote directory
            directory = raw_input('Copy iptables script in directory [default: /usr/bin]: ')

            # Default if no directory given
            if directory == '':
                directory = '/usr/bin'

            # Get IP of the host
            ip = checkCommands.getHostIp(host).strip('\n')
            if ip == -1:
                print 'Push rules failed : Could not get IP or hostname of host'
                return

            try:
                # Create temporary file with all the rules
                tempfile = open(configuration.basedir+configuration.datadir+'/nm-iptables.sh','w')

                # Try to get the start template for the script.
                try:
                    starttpl = open(configuration.basedir+configuration.tpldir+'/'+configuration.starttpl,'r')
                    for line in starttpl:
                        tempfile.write(str(line))
                except:
                    # If it fails doesn't matter. It just means there is not start template
                    pass
                # Write all the rules
                tempfile.write(str(showCommands.showAccessList(host,1)))
                # Close file
                tempfile.close()
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
                print "Push rules failed : Unable to create temporary file."
                return

            # scp our file
            subprocess.Popen([ '/usr/bin/scp', configuration.basedir+configuration.datadir+'/nm-iptables.sh', user+'@'+ip+':'+directory+'/' ]).wait()

            # If username is root
            if user == 'root':
                # Ask our user if he wants us to execute the script
                answer = '?'
                while answer != 'n' and answer != 'y':
                    answer = raw_input('Do you wish to execute the iptables script on the host ? [y/n]: ')

                if answer == 'y':
                    # Send a little command via SSH
                    subprocess.Popen([ '/usr/bin/ssh', user+'@'+ip, "'/bin/bash "+directory+"/nm-iptables.sh'" ]).wait()

            else:
                # Ask our user if he wants us to execute the script via sudo
                answer = '?'
                while answer != 'n' and answer != 'Y':
                    answer = raw_input('Do you wish to execute the iptables script via sudo on the host ? [Y/n]: ')

                if answer == 'Y':
                    # Send a little command via SSH using sudo
                    subprocess.Popen("/usr/bin/ssh "+user+"@"+ip+" 'sudo bash "+directory+"/nm-iptables.sh'", shell=True).wait()

            # Remove the temporary file
            os.remove(configuration.basedir+configuration.datadir+'/nm-iptables.sh')

        else:
            print 'Unknown host'
            return
    else:
        print 'Push rules failed : Too few arguments. Type help for help.'