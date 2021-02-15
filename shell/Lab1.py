#! /usr/bin/env python3

import os, sys, re

def main():
    
    while True: # This is trying to replicate what a shell actually does 
        
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())
            
        args = os.read(0, 1024) # The number of bytes that can be accepted
        
        if len(args) == 0:
            break # This exits while loop
        
        args = args.decode().split("\n")
        
        if not args:
            continue # This goes back to start of while loop
        
        for arg in args:
            inputHandler(arg.split())
            
def inputHandler(args):
  
    if len(args) == 0: # Nothing really happens here, return to main
        return
        
    if "exit" in args: 
        sys.exit(0)

    # This is the change directory
    elif "cd" == args[0]:
        try:
            if len(args)==1: # If cd is specified, reprompt the user
                return   
            else:
                os.chdir(args[1])
        except: # Does not existent
            os.write(1, ("cd %s: No such file or directory\n" % args[1]).encode())
    else:
        rc = os.fork()
        
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            executeCommand(args)
            sys.exit(0)

def executeCommand(args):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:
            pass
        
    os.write(2, ("%s: command not found\n" % args[0]).encode()) # There is command not found, print an error message
    sys.exit(0)

if '__main__' == __name__:
    main() 
