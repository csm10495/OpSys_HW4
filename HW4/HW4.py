#OpSys Homework 4
#Charles Machalow and theoretically others

import sys

#global time variable
time = 0

# ---> Work on this.
#Process List class
class cProcessList:
    #Constructor, makes a cProcessList Object
    #Give it the entire input file and it will
    #parse it and make the list of processes
    def __init__(self, input_file):
        pass
        #parse the input_file
        #save it to a List...
        #self._list = ...

    #DON'T ACCESS _list DIRECTLY, use accessors, etc..

#Process class
class Process:
    #Constructor, makes a Process Object
    def __init__(self, char, arrival_times, exit_times, needed_frames):
        self.char = char                      #Char representation
        self.needed_frames = needed_frames    #Number of frames needed each time
        self.arrival_times = arrival_times    #Times that the process enters
        self.exit_times = exit_times          #Times that the process exits

    #returns char
    def getChar(self):
        return self.char

    #retuns needed_frames
    def getNeededFrames(self):
        return self.needed_frames

    #return arrival_times list
    def getArrivalTimes(self):
        return self.arrival_times

    #returns the next arrival time
    #if none exists, return -1
    def getNextArrivalTime(self):
        if (getRemainingInstances() >= 1):
            return self.arrival_times[0]
        else:
            return -1

    #return exit times list
    def getExitTimes(self):
        return self.exit_times

    #Gets the number of times this process will run from now...
    def getRemainingInstances(self):
        if len(self.arrival_times) == len(self.exit_times):
            return len(self.needed_frames)
        else:
            print "ERROR: (len(arrival_times) == len(exit_times)) == False"
            return -1

    #pops the top of the arrival, exit, frames
    def popTop(self):
        if len(self.arrival_times) <= 0:
            print "ERROR: Attempting to popTop a done process, shouldn't happen"
            return None
        else:
            frames = self.needed_frames
            arrival = self.arrival_times.pop(0)
            exit = self.exit_times.pop(0)
            return arrival, exit, frames

#Memory structure with 1600 memory frames, first 80 are for the OS
class cMem:
    def __init__(self):
        self._memory = ["#"] * 80 + ["."] * (1600 - 80)
    pass

    #prints this cMem's contents (in rows of 80 max)
    def printCMem(self):
        global time

        print "Memory at time " + time + ":"
        str = ""
        for i in self._memory:
            str += i

        for j in [str[i:i+80] for i in range(0, len(str), 80)]:
            print j

    #removes all fragmentation from this cMem
    def defrag(self):
        global time

        print "Performing defragmentation..."
        
        had_empty = False #had empty memory yet
        processes = []
        for i in self._memory:
            if i == "#":
                continue
            elif i == ".":
                had_empty = True
            elif had_empty and not i == ".":
                processes.append(i)

        count = len(set(processes)) #should be the number of moved processes

        self._memory = filter(lambda a: a != ".", self._memory) #removes all "."s

        addcount = 0 #number of readded "."s (empty memory)
        while len(self._memory < 1600): #adds all extra "."s
            addcount = addcount + 1
            self._memory.append(".")

        print "Relocated " + str(count) + " processes to create a free memory block of " + str(addcount) + " units (" + str((addcount / 1600) * 100) + "% of total memory)."
        print "Defragmentation completed."
        print ""
        print "Memory at time" + str(time) + ":"
        self.printCMem()

        if len(self._memory) > 1600:
            print "ERROR: The defrag has resulted in more than 1600 memory frames, this should NEVER happen"

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
        # ---> work on this


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


#call necessary functions to run the simulation
def runSimulation(quiet, input_file, mode):
    cPL = cProcessList("""args go here""")  #Processes waiting
    ccPL = cProcessList("""args go here""") #Processes running (not currently waiting) (cCurrentProcessList)
    cM = cMem()
    # ---> work on this
    pass



startUp() #start the simulation
