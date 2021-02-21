#! /usr/bin/env python3

import os, sys, re
from myReadLine import readLine

def main():
    while True: # This is trying to replicate what a shell actually does, but the main reason why we use a while is because we get to keep going and write other commands
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())
            
        args = readLine() # We are using the readLine() found in the myReadLine.py
        
        if len(args) == 0:
            break # This exits while loop
        
        args = args.split("\n") 
        
        if not args:
            continue # This goes back to start of while loop
        
        for arg in args:
            inputHandler(arg.split())
            
def inputHandler(args):
    if len(args) == 0: # Nothing really happens here so then it would return to main
        return
        
    if "exit" in args: # So if I was to write exit, then the program would end
        sys.exit(0)

    # This is the change directory when used "cd"
    elif "cd" == args[0]:
        try:
            if len(args)==1: # If cd is specified then it would reprompt the user
                return   
            else:
                os.chdir(args[1])
        except: # If the directory does not existent
            os.write(1, ("cd %s: No such file or directory\n" % args[1]).encode())            
    else:
        rc = os.fork() # The purpose of forking is to create a new process ... (I'm gonna add more to this later)
        
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            executeCommand(args)
            sys.exit(0)

def executeCommand(args):
    for dir in re.split(":", os.environ['PATH']): # The path, takes in the path (checker)
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # This is where we execute the program
        except FileNotFoundError:
            pass
        
    os.write(1, ("%s: command not found\n" % args[0]).encode()) # If the command not found then we would print an error message
    sys.exit(0)

if '__main__' == __name__:
    main() 
    
