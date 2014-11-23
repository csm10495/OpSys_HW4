#OpSys Homework 4
#Charles Machalow and theoretically others

import sys

#call necessary functions to run the simulation
def runSimulation(quiet, input_file, mode):
    pass

#startup function
def startUp():
    quiet = False
    input_file = ""
    mode = ""
    if len(sys.argv) == 4:
        if sys.argv[1] == "-q":
            quiet = True
        else:
            print "USAGE: memsim [-q] <input-file> { first | best | next | worst }"
            sys.exit(0)
        input_file = sys.argv[2]
        mode = sys.argv[3]
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        mode = sys.argv[2]
    else:
        print "USAGE: memsim [-q] <input-file> { first | best | next | worst }"
        sys.exit(0)

    runSimulation(quiet, input_file, mode)


startUp() #start the simulation
