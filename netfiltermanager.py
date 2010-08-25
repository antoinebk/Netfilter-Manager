#! /usr/bin/python

# netfilterManager

__author__="Antoine Benkemoun"
__date__ ="$10 aout 2010 15:02:58$"
__name__ == "__main__"

# IMPORTS
import sys
import showCommands
import checkCommands
import addCommands
import writeCommands
import delCommands
import pushCommands

# GLOBAL VARIABLES
__mode__ = "base"
__selectedhost__ = 'none'
__selectedline__ = 0

# CLASS
class Welcome:
    def __init__(self):
        print ""
        print "Welcome to netfilterManager Program v0.1"
        print ""
        print "This program helps you manage iptables rules for many hosts."
        print "It can create iptables scripts from Cisco rules or from regular iptables rules."
        print ""
        print "Please enter the command. If you need help, you can use the help command."
        print ""

class Command:
        def __init__(self,command):

            # GLOBAL VARIABLE
            global __mode__
            global __selectedhost__
            global __selectedline__

            command_family = command.split()[0]

            #
            # LEVEL OF COMMANDS : BASE
            #

            if __mode__ == "base":

                # Help command
                if command_family == 'help':
                    print "Available commands are : add, del, exit, help, push, quit, show"

                # Exit command
                elif command_family == 'exit':
                    sys.exit(0)

                # Quit command
                elif command_family == 'quit':
                    sys.exit(0)

                # __mode__ add
                elif command_family == "add":
                    __mode__ = "add"

                # __mode__ show
                elif command_family == "show":
                    __mode__ = "show"

                # __mode__ del
                elif command_family == 'del':
                    __mode__ = 'del'

                # __mode__ push
                elif command_family == 'push':
                    __mode__ = 'push'

                # Default, error and propose help
                else:
                    print "Unknown command "+command_family+". Type help for help."

            #
            # LEVEL OF COMMANDS : DEL
            #

            elif __mode__ == 'del':

                # Help command
                if command_family == 'help':
                    print 'Available commands are : exit, help, host <name>, line <#>, quit, iptables <...>, iptables help, select <host>'

                # exit command
                elif command_family == 'exit':
                    # If no host selected
                    if __selectedhost__ == 'none':
                        # Return to base commands
                        __mode__ = 'base'

                    # If there is a selected host
                    else:
                        # If there is a selected line
                        if __selectedline__ != 0:
                            # Remove selected line
                            __selectedline__ == 0
                        else:
                            # Remove selected host
                            __selectedhost__ = 'none'

                # host command
                elif command_family == 'host':
                    # Check if number of arguments is correct
                    if len(command.split()) == 2:
                        # Give the variable a friendlier name
                        host = str(command.split()[1])
                        delCommands.delHost(host)
                    else:
                        print 'Usage : host <name>. Deletes the host in question.'

                # select command
                elif command_family == 'select':

                    # check if number of arguments is correct
                    if len(command.split()) == 2:
                        if checkCommands.checkIfHostsExists(command.split()[1]) == 1:
                            # Change prompt via global variable
                            __selectedhost__ = command.split()[1]
                        else:
                            print 'Select host failed : Host not found'
                    else:
                        print 'Usage : select <name>. Selects a host.'
                        
                # line command
                elif command_family == 'line':
                    # Check if host is selected
                    if __selectedhost__ != 'none':
                        # Check if number of arguments is correct
                        if len(command.split()) == 2:
                            delCommands.delLine(__selectedhost__,command.split()[1])
                        else:
                            print 'Usage : line <#>. Deletes all the rules on the line in question.'
                    else:
                        print 'You must select a host before selecting line.'

                # iptables command
                elif command_family == 'iptables':
                    if __selectedhost__ == 'none' and not (len(command.split()) <= 2 or command.split()[1] == 'help'):
                        print 'You must select a host before deleting rule'
                    elif len(command.split()) <= 2 or command.split()[1] == 'help':
                        print 'Usage : '
                        print ' 1. Select a host'
                        print ' 2. Type in the rule you want to delete'
                    else:
                        delCommands.delRule(__selectedhost__,command)

                # quit command
                elif command_family == 'quit':
                    sys.exit(0)

                # Unknow command
                else:
                    print "Unknown command "+command_family+". Type help for help"

            #
            # LEVEL OF COMMANDS : PUSH
            #

            elif __mode__ == 'push':

                # help command
                if command_family == 'help':
                    print 'Available commands are : exit, help, ssh <host>, quit'

                # exit command
                elif command_family == 'exit':
                    # Check if no host selected
                    if __selectedhost__ == 'none':
                        # Return to base commands
                        __mode__ = "base"

                    # If there is a selected host
                    else:
                        # If there is a selected line
                        if __selectedline__ != 0:
                            # Remove selected line
                            __selectedline__ = 0
                        else:
                            # Remove selected host
                            __selectedhost__ = 'none'

                # quit command
                elif command_family == 'quit':
                    sys.exit(0)

                # push command
                elif command_family == 'ssh':
                    # Send to pushCommandSSH
                    pushCommands.pushSSH(command)

                # default : error and propose help
                else:
                    print 'Unknown command '+command_family+'. Type help for help'

                
            #
            # LEVEL OF COMMANDS : ADD
            #

            elif __mode__ == "add":

                # Help command
                if command_family == "help":
                    print "Available commands are : access-list, access-list help, exit, help, host, iptables, iptables help, line <#>, quit, select <host>"

                # exit command
                elif command_family == "exit":
                    # Check if no host selected
                    if __selectedhost__ == 'none':
                        # Return to base commands
                        __mode__ = "base"

                    # If there is a selected host
                    else:
                        # If there is a selected line
                        if __selectedline__ != 0:
                            # Remove selected line
                            __selectedline__ = 0
                        else:
                            # Remove selected host
                            __selectedhost__ = 'none'

                # Quit command
                elif command_family == "quit":
                    sys.exit(0)
                    
                # Host command
                elif command_family == "host":
                    if len(command.split()) < 3:
                        print "Usage : add <name> <ip/hostname>. Adds the host."
                        
                    elif len(command.split()) == 3:

                        # Give the variables a friendlier name
                        hostname = command.split()[1]
                        ip = command.split()[2]

                        # Add host
                        addCommands.addHost(hostname,ip)
                            
                    else:
                        print 'Usage : add <name> <ip/hostname>'
               
                # select command
                elif command_family == 'select':

                    # check if number of arguments is correct
                    if len(command.split()) == 2:
                        if checkCommands.checkIfHostsExists(command.split()[1]) == 1:
                            # Change prompt via global variable
                            __selectedhost__ = command.split()[1]
                        else:
                            print 'Select host failed : Host not found'
                    else:
                        print 'Usage : select <name>. Selects a host.'

                # line command
                elif command_family == 'line':

                    # Check if number of arguments is correct
                    if len(command.split()) == 2:
                        # Check if host is selected
                        if __selectedhost__ != 'none':
                            # Check if argument is a number
                            if command.split()[1].isdigit():
                                # Check if line number >0 and <= 200
                                if int(command.split()[1]) > 0 and int(command.split()[1]) <= 200:
                                    __selectedline__ = command.split()[1]
                                else:
                                    print 'Line number must be greater then 0 and less then 200'
                            else:
                                print 'Line argument is not a number'
                        else:
                            print 'Must select a host before selecting line.'
                    else:
                        print 'Usage : line <linenumber>. Selects a line'


                # Access-list command
                elif command_family == "access-list":
                    if __selectedhost__ == 'none' and len(command.split()) >=2 and command.split()[1] != 'help':
                        print 'Access-list rule add failed : No host selected. Use "select" command.'
                    else:
                        # Send command to add-access-list function
                        rule = addCommands.addAccessList(command)

                        # Check if we got an iptables rules or an error
                        try:
                            if rule.split()[0] == 'iptables':
                                # Send rule to be written in host file
                                writeCommands.writeIptablesRule(__selectedhost__,__selectedline__,rule)
                        except:
                            # If we got an error, do nothing. Error message was already sent by previous function
                            pass

                # iptables command
                elif command_family == 'iptables':
                    if __selectedhost__ == 'none' and len(command.split()) >=2 and command.split()[1] != 'help':
                        print 'Iptables rule add failed : No host selected. Use "select" command.'
                    # iptables help
                    elif len(command.split()) == 1 or command.split()[1] == 'help':
                        print 'Insert an iptables rule as you would on a normal host'
                        print ' ex : iptables -A INPUT -s 192.168.0.0/24 -d 10.10.10.10 -j DROP'
                    else:
                        try:
                            # Directly send the rule to be writtent
                            writeCommands.writeIptablesRule(__selectedhost__,__selectedline__,command)
                        except:
                            # If we get an error, do nothing. Error message was already sent by previous function
                            pass

                # template command
                elif command_family == 'template':
                    # Check if host is selected
                    if __selectedhost__ == 'none':
                        print 'You must first select a host. Type help for help.'
                    else:
                        addCommands.addTemplateToHost(__selectedhost__,__selectedline__,command)

                # Default, error and propose help
                else:
                    print "Unknown command "+command_family+". Type help for help"

            #
            # LEVEL OF COMMANDS : SHOW
            #
            
            elif __mode__ == "show":

                # Help command
                if command_family == "help":
                    print "Availabe commands are : access-list <host>, exit, help, hosts, iptables <host>, quit, version"

                # exit command
                elif command_family == "exit":
                    # Return to base commands
                    __mode__ = "base"

                # Quit command
                elif command_family == "quit":
                    sys.exit(0)

                # Hosts command
                elif command_family == "hosts":
                    showCommands.showHosts()

                # Version command
                elif command_family == "version":
                    showCommands.showVersion()

                elif command_family == 'access-list':

                    # Check if argument count is correct
                    if len(command.split()) == 2 :

                        # Check if host exists
                        host = command.split()[1]
                        if checkCommands.checkIfHostsExists(host):

                            # show access-list for the host
                            showCommands.showAccessList(host,0)

                        else:
                            print 'Unknown host '+host

                    else:
                        print 'Usage : access-list <host>'

                elif command_family == 'iptables':

                    # Check if argument count is correct
                    if len(command.split()) == 2 :

                        # Check if host exists
                        host = command.split()[1]
                        if checkCommands.checkIfHostsExists(host):

                            # show access-list for the host
                            showCommands.showAccessList(host,0)

                        else:
                            print 'Unknown host '+host

                    else:
                        print 'Usage : iptables <host>'

                # Default, error and propose help
                else:
                    print "Unknown command "+command_family+". Type help for help"



            # Go back to previous prompt
            Prompt ()



class Prompt:

    # Function to check the command typed in
    def checknozero(self,command):
        # Check that command was typed in
        if not len(command) > 0:
            #Go back to prompt
            Prompt()


    def __init__(self):

        # GLOBAL VARIABLE
        global __mode__
        global __selectedhost__
        global __selectedline__

        # Default level of commands
        if __mode__ == "base":
            command = raw_input("> ")
            self.checknozero(command)
            Command(command)

        # Higher level of commands
        else:
            # Display name of selected host in prompt
            if __selectedhost__ == 'none':
                command = raw_input("("+__mode__+") > ")
            else:
                if __selectedline__ == 0:
                    command = raw_input("("+__mode__+"-"+__selectedhost__+") > ")
                else:
                    command = raw_input("("+__mode__+"-"+__selectedhost__+":"+__selectedline__+") > ")


            self.checknozero(command)
            Command(command)


# MAIN PROGRAM
if __name__ == "__main__":
    # Check if configuration was edited
    checkCommands.checkConfiguration()
    # Catch ctrl+c
    try:
        Welcome()
        Prompt()
    except (KeyboardInterrupt, SystemExit):
        print 'Exiting ...'
        sys.exit(0)


