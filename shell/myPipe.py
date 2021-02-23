import os, sys, write
from myRedirect import redirect

def piping(args):
    args = args.split('|')
    leftArg = args[0].split()
    rightArg = args[1].split()
    pipeRead, pipeWrite = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed\n").encode())
        sys.exit(1)
    elif rc == 0: # We will execute the left arg here
        if "<" in leftArg:
            redirect(leftArg)         
        if ">" in leftArg:
            redirect(leftArg)
            
    else: # Then we will execute the right arg here
        if "<" in rightArg:
            redirect(rightArg)
        if ">" in rightArg:
            redirect(rightArg)
            
