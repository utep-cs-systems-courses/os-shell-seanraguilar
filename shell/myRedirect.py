import os, sys, re

'''This function will check the direction (< or >) if it's the input or output, 
   then will return and pass the loop '''
def redirect(args):
    if '>' in args:
        os.close(1) # Close fd1
        os.open(args[args.index('>')+1], os.O_CREAT | os.O_WRONLY)# This creates file if there isnt one or wrtie to file
        os.set_inheritable(1,True)# This takes fd(0) and makes sure it is inheritable
        args.remove(args[args.index('>')+1])
        args.remove('>')
        
    elif '<' in args: 
        os.close(0) # This closes file descriptor 0 attached to standard input of keyboard
        os.open(args[args.index('<')+1], os.O_RDONLY) # Write only
        os.set_inheritable(0, True) # This is fd(0) which is attached to kbd
        args.remove(args[args.index('<') + 1])
        args.remove('<')
    
    for i in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (i, args[0])
        try:
            os.execve(program, args, os.environ) # Try to run
        except FileNotFoundError:
            pass # Couldn't find file so it passes
    
    os.write(2, ("%s command not found\n" % args[0]).encode()) # Writing the error message to display
    sys.exit(0)
