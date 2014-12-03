#OpSys Homework 4
#Charles Machalow, Colton Wicks (New Guy), Paul Horner
#"The Braintrust"

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
        self.last_allocated_index = 0         #index of last allocation for NEXT algorithm
        self._memory = ["#"] * 80 + ["."] * (1600 - 80)
    pass

    #prints this cMem's contents (in rows of 80 max)
    def printCMem(self):
        global time

        print "Memory at time " + str(time) + ":"
        memstr = ""
        for i in self._memory:
            memstr += i

        for j in [memstr[i:i + 80] for i in range(0, len(memstr), 80)]:
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
        while len(self._memory) < 1600: #adds all extra "."s
            addcount = addcount + 1
            self._memory.append(".")

        print "Relocated " + str(count) + " processes to create a free memory block of " + str(addcount) + " units (" + str((addcount / 1600) * 100) + "% of total memory)."
        print "Defragmentation completed."
        print ""
        print "Memory at time " + str(time) + ":"
        self.printCMem()

        if len(self._memory) > 1600:
            print "ERROR: The defrag has resulted in more than 1600 memory frames, this should NEVER happen"

    #removes a list of processes from this cMem
    def removeListOfProcesses(self, lst):
        for i in lst:
            self.removeProcess(i.getChar())

    #removes a given process from this cMem
    def removeProcess(self, process_char):
        for i in range(len(self._memory)):
            if self._memory[i] == process_char:
                self._memory[i] = "."

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

    #returns an index for cMem where it has num_frames available (starting at
    #index)
    def OLDgetNextAvailableLocation(self, num_frames, index):
        rotated_mem = self._memory
        rotated_mem = rotated_mem[index:] + rotated_mem[:index]   #rotate (shift) the array        
            
        string_rep = ""
        sub = ""
        count = 0
        print "ROTATED MEMORY"
        
        #This is wrong, it will split up contiguous memory
        #as if the defrag never happened
        for i in rotated_mem:
            string_rep += i
            sub += i
            count += 1
            if(count == 80):
                print sub
                count = 0
                sub = ""            

        loc = string_rep.find("." * int(num_frames)) 

        if loc == -1:
            return -1
        else:
            return loc + index % len(rotated_mem)
        
    def getNextAvailableLocation(self, num_frames, index):
        end = index
        inside = False
        count = 0
        currentBestIndex = -1
        currentSmallest = 1600
        i = index
        
        #we start from the given index, and go to the end
        #this means the given index can be in the middle of a contiguous 
        #section of "."s, so we need to call this again starting from the beginning
        #and going to the end
        while(i < 1600):            
            #we have not found a new "."
            if not inside and self._memory[i] == ".":
                inside = True
                count += 1
            #we are inside a string of "."s
            elif inside and self._memory[i] == ".":
                count += 1       
            #we are not/no longer inside, store and reset the important values
            else:
                inside = False
                count = 0             
            
            i += 1
            if count >= num_frames:
                return i - count   #perfect return            
            
        i = 80
        inside = False
        count = 0
        while(i < 1600):
            
            #we have not found a new "."
            if not inside and self._memory[i] == ".":
                inside = True
                count += 1
            #we are inside a string of "."s
            elif inside and self._memory[i] == ".":
                count += 1       
            #we are not/no longer inside, store and reset the important values
            else:
                inside = False
                count = 0                       
            
            i += 1     
            
            if count >= num_frames:
                return i - count
            
        return -1
            
                
 

    #returns an index for cMem where it has exactly num_frames available
    def getFirstAvailableExactLocation(self, num_frames):            
        #print str(num_frames)
        i = 80
        inside = False
        count = 0
        while(i < 1600):
            
            if not inside and self._memory[i] == ".":
                inside = True
                count = 1
            elif inside and self._memory[i] == ".":
                count += 1       
            else:
                if count == num_frames:
                    return i - count
                inside = False
                count = 0             
            
            i += 1

        return -1
    
    #returns an index for cMem where it has num_frames available
    def getBestAvailableLocation(self, num_frames):               
        i = 80
        inside = False
        count = 0
        
        currentBestIndex = -1
        currentSmallest = 1600
        while(i < 1600):
            
            #we have not found a new "."
            if not inside and self._memory[i] == ".":
                inside = True
                count += 1
            #we are inside a string of "."s
            elif inside and self._memory[i] == ".":
                count += 1       
            #we are not/no longer inside, store and reset the important values
            else:
                if count == num_frames:
                    return i - count   #perfect return
                inside = False
                count = 0                    
            
            i += 1
            
            #if we have found a better fit
            if count < currentSmallest and count >= num_frames:
                currentSmallest = count
                currentBestIndex = i - count
                
        return currentBestIndex  #nonperfect return

    #returns an index for cMem where it has num_frames available (worst)
    def getWorstAvailableLocation(self, num_frames):               
        i = 80
        inside = False
        count = 0
        
        currentWorstIndex = -1
        currentLargest = -1
        while(i < 1600):
            
            #we have not found a new "."
            if not inside and self._memory[i] == ".":
                inside = True
                count += 1
            #we are inside a string of "."s
            elif inside and self._memory[i] == ".":
                count += 1       
            #we are not/no longer inside, store and reset the important values
            else:
                inside = False
                count = 0      
            
            if count > currentLargest and count >= num_frames:
                currentLargest = count
                currentWorstIndex = i - count + 1            
            
            i += 1
        return currentWorstIndex  #nonperfect return
        
    def bestFit(self, num_frames):
        
        
        return empty_index
        
            
    #used to add a process to this cMem
    #add_method: noncontig | first | best | next | worst
    #process_char: Name of process (A-Z)
    #num_frames: Number of frames the process needs
    def addProcess(self, add_method, process_char, num_frames):

        #noncontiguous algorithm
        if add_method == "noncontig":
            if self.getNumFreeFrames() >= num_frames:
                frames_left = num_frames
                i = 80
                while frames_left > 0:
                    if self._memory[i] == ".":
                        self._memory[i] = process_char
                        frames_left -= 1
                    i+=1
            else:
                print"ERROR: Not enough memory for process."
                sys.exit(0)
        
        #first algorithm
        elif add_method == "first":
            if self.getNumFreeFrames() >= num_frames:
                #getFirstAvailableLocation will get the 'first' location in the
                #cMem that can store this many frames contiguously
                #if we have 5 empty spaces in a row but num_frames is 4
                #getFirst...  will return -1
                if self.getFirstAvailableLocation(num_frames) > 79:        
                    i = self.getFirstAvailableLocation(num_frames)
                    end = i + num_frames
                    while i < end:
                        self._memory[i] = process_char
                        if i > self.last_allocated_index:
                            self.last_allocated_index = i
                        i+=1
                else:#if there is enough room but is not contiguous defrag then find the first empty
                     #space in memory
                    self.defrag()
                    
                    i = self.getFirstAvailableLocation(num_frames)
                    end = i + num_frames
                    while i < end:
                        self._memory[i] = process_char
                        i += 1
                    self.last_allocated_index = end - 1
            else:
                print"ERROR: Not enough memory for process."
                sys.exit(0)
        
        #best algorithm
        elif add_method == "best":
            if self.getNumFreeFrames() >= num_frames:
                i = num_frames
                loc = self.getBestAvailableLocation(i)  #definite amount of space
                if(loc >= 0):
                    while num_frames != 0:
                        self._memory[loc] = process_char
                        num_frames = num_frames - 1
                        loc = loc + 1
                else:
                    self.defrag()
                    loc = self.getBestAvailableLocation(i) 
                    if loc >= 0:
                        while num_frames != 0:
                            self._memory[loc] = process_char
                            num_frames = num_frames - 1
                            loc = loc + 1
                    else:
                        print "ERROR: SPACE NOT FOUND AFTER DEFRAG. THIS SHOULD NOT HAPPEN"
                        sys.exit(0)
            else:
                print "ERROR: Not enough memory for process."
                sys.exit(0)
        
        #next algorithm
        elif add_method == "next":
            if self.getNumFreeFrames() >= num_frames:
                i = num_frames
                loc = self.getNextAvailableLocation(i, self.last_allocated_index)  #definite amount of space
                if(loc >= 0):
                    self.last_allocated_index = loc
                    while num_frames != 0:
                        self._memory[loc] = process_char
                        num_frames = num_frames - 1
                        loc = loc + 1
                else:
                    self.defrag()
                    loc = self.getNextAvailableLocation(i, self.last_allocated_index) 
                    print "loc after defrag:" + str(loc)
                    if loc >= 0:
                        self.last_allocated_index = loc
                        while num_frames != 0:
                            self._memory[loc] = process_char
                            num_frames = num_frames - 1
                            loc = loc + 1
                    else:
                        print "FAILURE AFTER DEFRAG: THIS SHOULDN'T HAPPEN"
            else:
                print "ERROR: Not enough memory for process."
                sys.exit(0)

        #worst algorithm
        elif add_method == "worst":
            if self.getNumFreeFrames() >= num_frames:
                i = num_frames
                loc = self.getWorstAvailableLocation(i)  #definite amount of space
                if(loc >= 0):
                    while num_frames != 0:
                        self._memory[loc] = process_char
                        num_frames = num_frames - 1
                        loc = loc + 1
                else:
                    self.defrag()
                    loc = self.getWorstAvailableLocation(i) 
                    if loc >= 0:
                        while num_frames != 0:
                            self._memory[loc] = process_char
                            num_frames = num_frames - 1
                            loc = loc + 1
            else:
                print "ERROR: Not enough memory for process."
                sys.exit(0)

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
            #print the current memory state
            cM.printCMem()
            
            userInput = raw_input("Run for: ")

            try:
                remaining = int(userInput)#todo: Error checking here
            except ValueError:
                print "ValueError: Hey ", userInput, " is not an int. I'm running the simulation forward 1."
                remaining = 1
            
            #if the user enters '0', we exit the program
            if remaining == 0:
                break                        
            
        #get the lists of arriving and exiting processes
        entryList = cPL.getProcessesThatShouldArriveNow()
        exitList = ccPL.getProcessesThatShouldExitNow()
        
        #process the processes that have just exited [BEFORE arrivals]
        for proc in exitList:
            proc.popTop()#we no longer need the current start/end time of this process
            print("Removing..." + proc.getChar() + "...at time: " + str(time))
            cM.removeProcess(proc.getChar())        
        
        #process the processes that have just arrived
        for proc in entryList:
            print("Adding..." + proc.getChar() + "...at time: " + str(time))
            cM.addProcess(mode, proc.getChar(), proc.getNeededFrames())
        
        #question: before or after the time has incremented
        #add the processes that just exited to the waiting list
        cPL.addListOfProcesses(exitList)
        
        #question: before or after the time has incremeted
        #add the processes that just started to the running list
        ccPL.addListOfProcesses(entryList)
        
        print("Time..." + str(time))
        
        remaining -= 1        
        time += 1
        
    print("Exiting")



startUp() #start the simulation
