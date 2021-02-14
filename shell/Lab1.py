#r/bin/env python3

import os, sys, re


def main():
    while True: # This is trying to replicate what a shell actually does
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())

        args = os.read(0, 1024) # This is the amount of bytes allowed in a statement or command

        if len(args) == 0: # If there is no command in the shell
            break # Then the program ends/exits the while loop

        args = args.decode().split("\n")

        if not args: 
            continue # Which goes back to start of while loop to continue

        for arg in args:
            inputHandler(arg.split()) # By using this command we are able to
                                      # handle with the commands that were inputted 

                                      
def inputHandler(args):
    if len(args) == 0: # So if there is no argument then nothing will happen and return to the main
        return

    if "exit" in args:
        sys.exit(0)

    # Here we are changing the directory
    elif "cd" == args[0]:
        try:
            if len(args)==1: # This is here if cd is specified then reprompt the user
                return

            else:
                os.chdir(args[1])

        except: # It does not exist
            os.write(1, ("cd %s: No such file or directory\n" % args[1]).encode())

    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:
            executeCommand(args)
            sys.exit(0)


def executeCommand(args): # This is where we get to execute the command
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ) # Trying to exec program

        except FileNotFoundError:
            pass

    # The command was not found and prints an error message
    os.write(2, ("%s: command not found\n" % args[0]).encode())
    sys.exit(0)


if '__main__' == __name__:
    main() 
