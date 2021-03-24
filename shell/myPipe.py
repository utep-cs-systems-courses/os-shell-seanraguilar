import os
from myRedirect import redirect
from shell import executeCommands
import pipe

'''This is the pipes method that take output of one method as input of another for example: output | input'''
def pipeInput(args): 
    left = args[0:args.index("|")] # This gets data of left side of pipe
    right = args[len(left)+1:] # This will get the data of right side of pipe
    pRead, pWrite = os.pipe() # This is making the read and write 
    rc = os.fork() # This creates a child process
    if rc < 0:# if the returns a 0 the for failed
        os.write(2, ("Fork has failed returning now %d\n" %rc).encode())#
        sys.exit(1)# This is used to exit
    
    elif rc == 0: # if return value is 0 do the following
        os.close(1) # This will close file descriptor 1
        os.dup(pWrite) # This copies the file descriptors of the child and put into pipeWrite
        os.set_inheritable(1,True)
        for fd in (pRead,pWrite):
            os.close(fd) # This closes all the file descriptors
        executeCommands(left) # This inputs the left argument into executeCommands
    
    else:
        os.close(0) # This closes file descriptor 0
        os.dup(pRead) # Then copies the files descriptor of the parent and puts it into pRead
        os.set_inheritable(0,True)
        for fd in (pWrite, pRead):
            os.close(fd) # This closes file descriptors in both pRead,pWrite
        if "|" in right: # if it finds '|' on the right side of argument then it pipes right vars
            pipe(right) # Then goes into pipe 
        executeCommands(right) # The inputs the right argument executeCommands
