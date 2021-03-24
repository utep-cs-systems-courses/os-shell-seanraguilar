import os, sys, re
from myReadLine import readLine
from myRedirect import redirect
#from myPiping import pipeInput

def main():
    '''This is trying to replicate what a shell actually does, but the main reason why we use a while is because we get to keep going and write other commands'''
    while True:
        if 'PS1' in os.environ:
            os.write(1,("$ ").encode())
        else:
            os.write(1, ("$ ").encode())
            
        args = readLine() # We are using the readLine() found in the myReadLine.py
        #args = read(0, 1024)
       
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
        except: # If the directory does not exist
            os.write(1, ("cd %s: No such file or directory\n" % args[1]).encode())            
    else:
        rc = os.fork() # The purpose of forking is to create a new process 
        
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
           # if ">" in args: # Check for redirect
            #    redirect(args)
            #if "<" in args:
             #   redirect(args)
            
            # These are meant for checking with direction inside the input
            executeCommand(args)
            sys.exit(0)
            
def executeCommand(args):
    if '|' in args: #check for pipe here so we can split in pipe()
            pipeInput(args)
            
    elif "/" in args[0]:
        program=args[0]
        try:
            os.execve(program,args,os.environ)#execute a process with enviornment
        except FileNotFoundError:
            pass
    elif ">" in args or "<" in args: #check for redirection
        redirect(args)
    else:
        for dir in re.split(":", os.environ['PATH']):#breaks the path apart by pattern of : in the environment variable path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)#tries to execute with given the parameters of program as path, args as arguments and os.environ as environment
            except FileNotFoundError:
                pass
    os.write(2, ("%s: command not found\n" % args[0]).encode())#error code 
    sys.exit(0)

def pipeInput(args):#the pipes method thats output of one program as input of another
    left=args[0:args.index("|")]# gets data of left side of arguments before |
    right=args[args.index("|")+1:]#gets the data of right side of arguments after |
    pRead, pWrite = os.pipe()#read and write 
    rc=os.fork()#creates a child 
    if rc<0:
        os.write(2, ("Fork has failed returning now %d\n" %rc).encode())#
        sys.exit(1)
    elif rc==0:#if return value is 0 do the following
        os.close(1)#close file descriptor 1
        os.dup(pWrite)#copies the file descriptors of the child into pWrite
        os.set_inheritable(1,True)#
        for fd in (pRead,pWrite):
            os.close(fd)#closes all the file descriptors
        executeCommand(left)#inputs the left argument to executeCommands
    else:
        os.close(0)#closes file descriptor 0
        os.dup(pRead)#copies the files descriptor of the parent and puts it into pRead
        os.set_inheritable(0,True)#
        for fd in (pWrite, pRead):
            os.close(fd)#closes file descriptors in both pRead,pWrite
        if "|" in right:#if it finds '|' on the right side of argument then it's piping it with right's varaibles
            pipe(right)#goes into pipe with variable right
        executeCommand(right)#inputs the right argument into commands

if '__main__' == __name__:
    main() 
