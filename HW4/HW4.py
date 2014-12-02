#OpSys Homework 4
#Charles Machalow and theoretically others

import sys

#global time variable
time = 0

#Process List class
class cProcessList:
    #Constructor, makes a cProcessList Object
    #Give it the entire input file and it will
    #parse it and make the list of processes
    def __init__(self, input_file=None):
        self._plist = []
        #if we are moking this cProcessList from the input_file, parse it
        if not input_file == None:
            f = open(input_file)
            num_processes = -1  #this doesn't really matter

            count = 0
            for line in f:
                if count == 0:
                    num_processes = int(line)
                    count = count + 1
                    continue
                else:
                    tmp_process_list = line.split()
                    char = tmp_process_list[0]
                    frames = int(tmp_process_list[1])
                    arrivals = []
                    exits = []

                    kount = 0
                    arrival = True
                    for i in tmp_process_list:
                        if kount < 2:
                            kount = kount + 1
                            continue
                        elif arrival:
                            arrival = False
                            arrivals.append(tmp_process_list[kount])
                        else:
                            arrival = True
                            exits.append(tmp_process_list[kount])

                        kount = kount + 1

                self._plist.append(Process(char, arrivals, exits, frames))
                count = count + 1

    #returns all processes that should arrive now
    #this also removes them from this cProcessList
    def getProcessesThatShouldArriveNow(self):
        global time
        
        now_processes = []
        for i in self._plist:
            if int(i.getNextArrivalTime()) == time:
                now_processes.append(i)
        
        for i in now_processes:
            self._plist.remove(i)   #i think this works, though it might not

        return now_processes

    #returns all processes that should exit now
    #this also removes them from this cProcessList
    def getProcessesThatShouldExitNow(self):
        global time

        now_processes = []
        for i in self._plist:
            if int(i.getNextExitTime()) == time:
                now_processes.append(i)
        
        for i in now_processes:
            self._plist.remove(i)   #i think this works, though it might not

        return now_processes

    #adds a Process to this cProcessList
    def addProcess(self, proc):
        self._plist.append(proc)

    #add a list of Processes to this cProcessList
    def addListOfProcesses(self, lst):
        for i in lst:
            if i.getNextArrivalTime() != -1:
                self._plist.append(i)

    #removes a Process from this cProcessList
    def removeProcess(self, proc):
        self._plist.remove(proc)
        
    def hasProcesses(self):
        return len(self._plist) != 0

#Process class
class Process:
    #Constructor, makes a Process Object
    def __init__(self, char, arrival_times, exit_times, needed_frames):
        self.char = char                      #Char representation
        self.needed_frames = needed_frames    #Number of frames needed each time
        self.arrival_times = arrival_times    #Times that the process enters
        self.exit_times = exit_times          #Times that the process exits

    #equality checker
    def __eq__(self, other):
        return self.char == other.char

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
        if (self.getRemainingInstances() >= 1 and len(self.arrival_times) > 0):
            return self.arrival_times[0]
        else:
            return -1

    #returns the next exit time
    #if none exists, return -1
    def getNextExitTime(self):
        if (self.getRemainingInstances() >= 1 and len(self.exit_times) > 0):
            return self.exit_times[0]
        else:
            return -1

    #return exit times list
    def getExitTimes(self):
        return self.exit_times

    #Gets the number of times this process will run from now...
    def getRemainingInstances(self):
        if len(self.arrival_times) == len(self.exit_times):
            return self.needed_frames
        else:
            return -1

    #pops the top of the arrival, exit, frames
    def popTop(self):
        if len(self.arrival_times) <= 0:
            print "ERROR: Attempting to popTop a done process, shouldn't happen"
            return None
        else:             
            arrival = self.arrival_times.pop(0)    
            exit = self.exit_times.pop(0)                
            frames = self.needed_frames
            return arrival, exit, frames #not used yet...
 

#Memory structure with 1600 memory frames, first 80 are for the OS
class cMem:
    def __init__(self):
        self.last_allocated_index = 79         #index of last allocation for NEXT algorithm
        self._memory = ["#"] * 80 + ["."] * (1600 - 80)
    pass

    #prints this cMem's contents (in rows of 80 max)
    def printCMem(self):
        global time

        print "Memory at time " + time + ":"
        str = ""
        for i in self._memory:
            str += i

        for j in [str[i:i + 80] for i in range(0, len(str), 80)]:
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

    #removes a list of processes from this cMem
    def removeListOfProcesses(self, lst):
        for i in lst:
            self.removeProcess(i.getChar())

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

    #returns an index for cMem where it has num_frames available
    def getFirstAvailableLocation(self, num_frames):
        string_rep = ""
        for i in self._memory:
            string_rep += i

        return string_rep.find("." * int(num_frames))
        #returns index on success, else returns -1
        
    def bestFit(self, num_frames):
        i=80
        count = 0
        empty_index = 0
        return empty_index
        
            
    #used to add a process to this cMem
    #add_method: noncontig | first | best | next | worst
    #process_char: Name of process (A-Z)
    #num_frames: Number of frames the process needs
    #return True if it worked, False if it didn't
    def addProcess(self, add_method, process_char, num_frames):
        # DON'T FORGET TO UPDATE self.last_allocated_index
        # ALSO, USE IT FOR NEXT

        #noncontiguous algorithm
        if add_method == "noncontig":
            if self.getNumFreeFrames()>=num_frames:
                frames_left = num_frames
                i = 80
                while frames_left > 0:
                    if self._memory[i] == ".":
                        self._memory[i] = process
                        frames_left -= 1
                    if i > self.last_allocated_index:
                        self.last_allocated_index = i
                    i+=1
            else:
                print"ERROR: Not enough memory for process."
        
        #first algorithm
        elif add_method == "first":
            if self.getNumFreeFrames()>=num_frames:
                if self.getFirstAvailableLocation(num_frames)>79:
                    i = self.getFirstAvailableLocation(num_frames)
                    end = i + num_frames
                    while i < end:
                        self._memory[i] = process_char
                        if i > self.last_allocated_index:
                            self.last_allocated_index = i
                else:#if there is enough room but is not contiguous defrag then find the first empty space in memory
                    self.defrag()
                    i=self.getFirstAvailableLocation(num_frames)
                    end = i+num_frames
                    while i < end:
                        self._memory[i] = process_char
                    self.last_allocated_index = end - 1
            else:
                print"ERROR: Not enough memory for process."
        
        #best algorithm
        elif add_method == "best":
            if self.getNumFreeFrames()>=num_frames:
                if getFirstAvailableLocation(num_frames)>79:
                    i = self.getFirstAvailableLocation(num_frames)
                    
                else:#if there is enough room but is not contiguous defrag then find the first empty space in memory
                    self.defrag()
                    i=self.getFirstAvailableLocation(num_frames)
                    end = i+num_frames
                    while i < end:
                        self._memory[i] = process_char
                    self.last_allocated_index = end - 1
            else:
                print"ERROR: Not enough memory for process."
        
        #next algorithm
        elif add_method == "next":

            if self.getNumFreeFrames()>=num_frames:# check to see if there is enough space over all

                i = self.last_allocated_index + 1
                if i+num_frames<len(self._memory):#if enough space at end put process there
                    end = self.last_allocated_index + num_frames#index of the last frame that was added
                    while i < end:
                        self._memory[i] = process_char
                        i+=1
                    self.last_allocated_index += num_frames#updates the last allocated index
                else:
                    if self.getFirstAvailableLocation(num_frames)>79:#sees if there is a space big enough between processes
                        i=self.getFirstAvailableLocation(num_frames)#sets i equal to the first empty space in memory big enough to store the process
                        end = i+num_frames
                        while i < end:#add procees to memory
                            self._memory[i] = process_char
                            i+=1
                    else:#if there is enough room but is not contiguous defrag then find the first empty space in memory
                        self.defrag()
                        i=self.getFirstAvailableLocation(num_frames)
                        end = i+num_frames
                        while i < end:
                            self._memory[i] = process_char
                        self.last_allocated_index = end - 1
            else:
                print"ERROR: Not enough memory for process."
        
        #worst algorithm
        elif add_method == "worst":
            if self.getNumFreeFrames()>=num_frames:
                pass
            else:
                print"ERROR: Not enough memory for process."

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
    global time
    
    cPL = cProcessList(input_file)  #Processes waiting
    ccPL = cProcessList() #Processes running (not currently waiting) (cCurrentProcessList)
    cM = cMem()
    # ---> work on this
    
    remaining = 0
    
    # while there are remaining processes to process
    while cPL.hasProcesses() or ccPL.hasProcesses():
        
        #if the user wants to specify the next time slice
        if not quiet and remaining <= 0:
            userInput = raw_input("Run for:")
            remaining = int(userInput)#todo: Error checking here
            
            if remaining == 0:
                break                        
            
        entryList = cPL.getProcessesThatShouldArriveNow()
        exitList = ccPL.getProcessesThatShouldExitNow()
        
        if len(entryList) != 0:
            print("Entry found...")
        
        for proc in exitList:
            proc.popTop()#we no longer need the current start/end time of this process
            print("Removing..." + proc.getChar() + "...at time:" + str(time))
            cM.removeProcess(proc.getChar())        
        
        for proc in entryList:
            print("Adding..." + proc.getChar() + "...at time:" + str(time))
            cM.addProcess(mode, proc.getChar(), proc.getNeededFrames())
        
        #question: before or after the time has incremented
        cPL.addListOfProcesses(exitList)#add the processes that just exited to the waiting list
        
        #question: before or after the time has incremeted
        ccPL.addListOfProcesses(entryList)#add the processes that just started to the running list
        
        #print("Time..." + str(time) + "   Remaining..." + str(remaining))
        
        remaining -= 1        
        time += 1
        
    print("Exiting")



startUp() #start the simulation
