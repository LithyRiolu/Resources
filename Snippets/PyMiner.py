import os, sys, math
try:
    import psutil
except:
    print("Unable to import psutil. Please run the following command to install it\n\tpython3 -m pip install psutil\nand restart this program.")
    exit()
try:
    import thread
except:
    import _thread as thread

_RUNNING = False

def inp(text):
    try: # Py2
        return(raw_input(text))
    except: # Py3
        return(input(text))

def restart():
    kill()
    call(config_read())

def clear():
    try:
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system('clear')
        else:
            os.system('cls')
    except:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')


def kill():
    for process in psutil.process_iter():
        if('miner' in str(process.name)):
            psutil.Process(int(str(process.pid))).terminate()



def call(values):
    global _RUNNING
    _RUNNING = True 
    if sys.platform == "linux" or sys.platform == "linux2":
        thread.start_new_thread(os.system,("./miner --threads {} --log-level {} --address {}".format(values[0], values[1], values[2]),))
    else:
        thread.start_new_thread(os.system,("miner.exe --threads {} --log-level {} --address {}".format(values[0], values[1], values[2]),))


def write(values):
    if sys.platform == "linux" or sys.platform == "linux2":
        open("config.txt","w").write("threads {:s}\nlog-level {:s}\naddress {:s}".format(values[0],values[1],values[2]))
    else:
        open("config.txt","w").write("threads {:s}\r\nlog-level {:s}\r\naddress {:s}".format(values[0],values[1],values[2]))


def config_read():
    values = [0,0,0]
    f = [x.split(' ') for x in open("config.txt","r").read().replace('\r\n','\n').split('\n')]
    temp = 0
    for x in f:
        if x[0] == "threads":
            values[0] = x[1]
            temp += 1
            continue
        if x[0] == "log-level":
            values[1] = x[1]
            temp += 1
            continue
        if x[0] == "address":
            values[2] = x[1]
            temp += 1
            continue
    if temp <3: # A <3 for our users
        raise Exception("Null")
    return(values)


def help():
    print("e | exit            -\tCloses miner and program")
    print("h | hashrate        -\tEnables hashrate output")
    print("p | pause           -\tPauses miner")
    print("r | resume          -\tRestarts miner")
    print("l | set_log x       -\tSets log-level to x")
    print("t | set_threads x   -\tSets number of threads to x")


def create_config(values):
    while True:
        values[0] = request("How many threads should be used?", int(math.ceil(psutil.cpu_count()*3/4)), "We recommend to use 3/4 times your total core count as a thread count. \nFor example, an octacore CPU should use six or seven threads.", "int")
        if values[1] < 6 and values[1] >= 0:
            break
        print("Please enter a number between one and {:d} (incusive). Recommended is {:d}".format(psutil.cpu_count(), int(math.ceil(psutil.cpu_count()*3/4))))
    while True:
        values[1] = request("Which log-level should be used?", 0, "0\tCritical error messages, aborts the subsystem\n\n1\tMajor error messages, some lost functionality\n\n2\tWarning error messages which do not cause a functional failure\n\n3\tInformational messages, showing completion, progress, etc.\n\n4\tDebug messages, to help in diagnosing a problem\n\n5\tTrace messages (enter/exit subroutine, buffer contents, etc.)", "int")
        if values[1] < 6 and values[1] >= 0:
            break
        print("Please enter a number between zero and five (incusive).")
    values[2] = request("Enter your wallet address please.", "", "You wallet address will be displayed in your wallet at startup.\nIt is 95 characters long and starts with a '1'", "wallet")
    return (values)

def request(question, default, helpmessage, typ):
    while True:
        if default == '':
            default_str = ''
        else:
            default_str = "Default: {} | ".format(str(default))
        temp = inp(question + " [{:s}? for help]\n".format(default_str))
        print("\n")
        if typ == "int":
            try:
                temp = int(temp)
                break
            except:
                print("\n")
                if (temp == '?') or (temp.lower() == 'h'):
                    print(helpmessage)
                    continue
                if temp == '':
                    temp = int(default)
                    continue
                print("Could not process your input. Please make sure, it is an integer.\n")
                continue
        if typ == "wallet":            
            if (temp == '?') or (temp.lower() == 'h'):
                print(helpmessage)
                continue
            if len(temp) != 95:
                print("The entered address has an invalid lenght")
                continue
            if list(temp)[0] != '1':
                print("Invalid first character")
                continue
            break
        print("Could not determine the type of the output")
    clear()
    return temp   


def ui(RUNNING):
    i = str(inp("\n")).lower()
    if len(i) == 0:
        help()
        return
    elif i == "exit" or i[0] == 'e':
        if(RUNNING):
            kill()
        sys.exit(1)
    try:
        if i[0:7] == "set_log" or i[0] == 'l':
            try:
                try:
                    level = int(i[8:])
                except:
                    level = int(i[2:])
                if level < 6 and level >= 0:
                    values = config_read()
                    write([values[0], str(level), values[2]])
                else:
                    raise Exception("Null")
                if(RUNNING):
                    restart()
                return
            except:
                print("Please enter a number between zero and five (incusive).")
            return
    except:
        pass
    try:
        if i[0:11] == "set_threads" or i[0] == 't':
            try:
                try:
                    threads = int(i[12:])
                except:
                    threads = int(i[2:])
                if threads <= psutil.cpu_count() and threads > 0:
                    values = config_read()
                    write([str(threads), values[1], values[2]])
                else:
                    raise Exception("Null")
                if(RUNNING):
                    restart()
                return
            except:
                print("Please enter a number between one and {:d} (incusive). Recommended is {:d}".format(psutil.cpu_count(), int(math.ceil(psutil.cpu_count()*3/4))))
            return
    except:
        pass
    try:
        if i[0:5] == "pause" or i[0] == 'p':
            kill()
            print("Paused the miner. Enter 'resume' to resume.")
            global _RUNNING
            _RUNNING = False
            return
    except:
        pass
    try:
        if i[0:6] == "resume" or i[0] == 'r':
            call(config_read())
            print("Restarted the miner.")
            return
    except:
        pass
    try:
        if i[0:4] == 'hashrate' or i[0] == 'h':
            values = config_read()
            if(int(values[1]) < 3):
                print("Enabling log-level 3 to display hashrate")
                write([values[0], '3', values[2]])
                restart()
            else:
                print("To optimise hashrate output, it's recommended to set the log-level to 3.")
            return
    except:
        pass    


    


def init():
    try:
        values = config_read()
    except:
        values = create_config([0,0,0])
        values = [str(v) for v in values]
        write(values)    
    return(values)



values = init()
call(values)
while True:
    ui(_RUNNING)
