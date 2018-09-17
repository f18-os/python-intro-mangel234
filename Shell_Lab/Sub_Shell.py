#! /usr/bin/env python3
# Modified by Miguel Nunez
# Date: Sep 16, 2018
import os, sys, time, re

pid = os.getpid()  # get and remember pid
# os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
next_input = ["null"]

print('[Sub@Wolvez]$\n')

while next_input[0] != 'exit':
    next_input = input().split()
    args = next_input[0:]  # Grab all the arguments
    # Debugging
    # Keep on asking for user arguments
    # print('Input[0] -> ' + next_input[0])
    # print('Arguments ' + str(args))
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:  # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())

        os.close(1)  # redirect child's stdout
        sys.stdout = open("p4-output.txt", "w")
        fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        # os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
            program = "%s/%s" % (dir, next_input[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)  # terminate with error

    else:  # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())
