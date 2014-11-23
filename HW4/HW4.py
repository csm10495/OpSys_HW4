#OpSys Homework 4
#Charles Machalow and theoretically others

import sys


#Memory structure with 1600 memory frames, first 80 are for the OS
class cMem:
    def __init__(self):
        self._memory = ["#"] * 80 + ["."] * (1600 - 80)
    pass

    #prints this cMem's contents
    def printCMem(self):
        str = ""
        for i in self._memory:
            str += i
        print str

    #removes a given process from this cMem
    def removeProcess(self, process_char):
        for i in self._memory:
            if i == process_char:
                i = "."

    #returns the number of empty spaces in this cMem
    def getNumFreeFrames(self):
        count = 0
        for i in self._memory:
            if i == ".":
                count = count + 1
        return count

    #used to add a process to this cMem
    #add_method: noncontig | first | best | next | worst
    #process_char: Name of process (A-Z)
    #num_frames: Number of frames the process needs
    #return True if it worked, False if it didn't
    def addProcess(self, add_method, process_char, num_frames):
        return False

#call necessary functions to run the simulation
def runSimulation(quiet, input_file, mode):
    a = cMem()
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
            print "USAGE: memsim [-q] <input-file> { noncontig | first | best | next | worst }"
            sys.exit(0)
        input_file = sys.argv[2]
        mode = sys.argv[3]
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        mode = sys.argv[2]
    else:
        print "USAGE: memsim [-q] <input-file> { noncontig | first | best | next | worst }"
        sys.exit(0)

    runSimulation(quiet, input_file, mode)


startUp() #start the simulation
