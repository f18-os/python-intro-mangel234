#! /usr/bin/env python3
# Modified by Miguel Nunez
# Date: Sep 16, 2018
import os, sys, time, re

# os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
next_input = ["null"]

# print('[Sub@Wolvez]$\n')

while next_input[0] != 'exit':
    print('[Sub@Wolvez]$')
    next_input = input().split()
    args = next_input  # Grab all the arguments
    # Debugging
    # Keep on asking for user arguments
    # print('Input[0] -> ' + next_input[0])
    # print('Arguments ' + str(args))
    pid = os.getpid()  # get and remember pid
    rc = os.fork()

    temp = ""
    try:
        for i in range(len(args)):
            if args[i] == '>':
                temp = args[i + 1]
                os.close(1)
                sys.stdout = open(temp, 'w')
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                # grab everything that you have besides the '>'
                args = args[:i]

    except IndexError as err:
        pass
        # print("OS error: {0}".format(err))

    if rc < 0:
        # os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:  # child
        # os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
        #       (os.getpid(), pid)).encode())

        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
            program = "%s/%s" % (dir, next_input[0])
            # print(str(program))
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        # os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)  # terminate with error

    # else:  # parent (forked ok)
    # os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
    #   (pid, rc)).encode())
    # childPidCode = os.wait()
    # os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
    #   childPidCode).encode())
