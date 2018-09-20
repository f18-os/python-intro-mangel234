#! /usr/bin/env python3
# Modified by Mystic
# Date: Sep 16, 2018
import fileinput
import os, sys, time, re

next_input = ["null"]
pid = os.getpid()  # get and remember pid
# Flag to check if we are in a pip argument
pipeCharacter = False
# sos.environ.get()
sleeping = False
if 'PS1' in os.environ:
    ps1 = os.environ('PS1')
else:
    ps1 = "[Sub@Wolvez]$ "

while next_input[0] != 'exit':

    next_input = input(ps1).split()
    args = next_input  # Grab all the arguments

    # Handle cd
    for i in range(len(args)):
        if args[i] == 'cd':
            # get location of directory
            directory = os.getcwd()
            # print(directory)
            directory = directory.split("/")
            # change directory
            os.chdir(next_input[i + 1])

    # Dont fork if not using cd
    rc = os.fork()
    # Handle  redirections
    temp = ""
    try:
        for i in range(len(args)):
            # Grabbing  output redirect
            if args[i] == '>':
                temp = args[i + 1]
                os.close(1)
                sys.stdout = open(temp, 'w')
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                # grab everything that you have besides the '>'
                args = args[:i]

            # Grabbing input redirect
            if args[i] == '<':
                temp = args[i + 1]
                os.close(0)
                # Use stdin now to do the opposite
                sys.stdin = open(temp, 'r')
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)
                args = args[:i]
                # grab everything that you have besides the '>'
            if args[i] == '|':
                pipeCharacter = True
                args = args[:i]
            if args[i] == '&':
                sleeping = True
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
    else:
        if sleeping:
            childPidCode = os.wait()

        # os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        # sys.exit(1)  # terminate with error

        # This handles the piping below
    if pipeCharacter:
        for i in range(len(args)):
            if args[i] == '|':
                temp = args.split('|')
                # Grab the two arguments
                firstPart = temp[0]
                secondPart = temp[1]

                pr, pw = os.pipe()
                for f in (pr, pw):
                    os.set_inheritable(f, True)
                #  print("pipe fds: pr=%d, pw=%d" % (pr, pw))
                # print("About to fork (pid=%d)" % pid)

                rk = os.fork()

                if rk < 0:
                    # print("fork failed, returning %d\n" % rk, file=sys.stderr)
                    sys.exit(1)

                elif rk == 0:  # child - will write to pipe
                    # print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
                    os.close(1)  # redirect child's stdout
                    os.dup(pw)
                    for fd in (pr, pw):
                        os.close(fd)

                    fd = sys.stdout.fileno()
                    os.set_inheritable(fd, True)

                    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                        program = "%s/%s" % (dir, firstPart)
                        # print(str(program))
                        try:
                            os.execve(program, firstPart, os.environ)  # try to exec program
                        except FileNotFoundError:  # ...expected
                            pass  # ...fail quietly

                    rt = os.fork()

                    if rt < 0:
                        # print("fork failed, returning %d\n" % rt, file=sys.stderr)
                        sys.exit(1)

                    elif rt == 0:  # child - will write to pipe
                        # print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
                        os.close(0)  # redirect child's stdout
                        os.dup(pr)
                        for fd in (pr, pw):
                            os.close(fd)

                        fd = sys.stdin.fileno()
                        os.set_inheritable(fd, True)

                        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                            program = "%s/%s" % (dir, secondPart)
                            # print(str(program))
                            try:
                                os.execve(program, secondPart, os.environ)  # try to exec program
                            except FileNotFoundError:  # ...expected
                                pass  # ...fail quietly
                    # Below is else
                    else:
                        os.dup(pr)
                        for fd in (pr, pw):
                            os.close(fd)
                        # print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rt), file=sys.stderr)
                        # os.close(0)
                        # os.dup(pr)
                        # for fd in (pw, pr):
                        #     os.close(fd)
                        #
                        # fd = sys.stdin.fileno()
                        # os.set_inheritable(fd, True)
                        #
                        # for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                        #     program = "%s/%s" % (dir, secondPart)
                        #     # print(str(program))
                        #     try:
                        #         os.execve(program, args, os.environ)  # try to exec program
                        #     except FileNotFoundError:  # ...expected
                        #         pass  # ...fail quietly
                # for line in fileinput.input():
                # print("From child: <%s>" + str(line))
